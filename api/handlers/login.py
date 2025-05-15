import logging
import os
import binascii
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidKey
from tornado.escape import json_decode
from tornado.gen import coroutine
from uuid import uuid4
from datetime import datetime, timedelta
from time import mktime
from .base import BaseHandler

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

class LoginHandler(BaseHandler):

    @coroutine
    def generate_token(self, email):
        try:
            # Generate a token UUID and expiration time
            token_uuid = uuid4().hex
            expires_in = datetime.now() + timedelta(hours=2)
            expires_in = mktime(expires_in.utctimetuple())

            token = {
                'token': token_uuid,
                'expiresIn': expires_in,
            }

            # Log the generated token for debugging
            logging.debug(f"Generated token: {token}")

            # Update token in the database
            result = yield self.db.users.update_one({
                'email': email
            }, {
                '$set': token
            })

            # Log the result of the update operation
            logging.debug(f"Update result: {result}")

            # Check if the update was successful
            if result.matched_count == 0:
                logging.error(f"No matching user found for token update for email: {email}")
                self.send_error(500, message="User not found during token generation")
                return None
            elif result.modified_count == 0:
                logging.error(f"User found but token not updated for email: {email}")
                self.send_error(500, message="Token update failed")
                return None

            return token
        except Exception as e:
            # Log the error if token generation fails
            logging.error(f"Error generating token for {email}: {e}")
            self.send_error(500, message="Error generating token")
            return None

    @coroutine
    def post(self):
        try:
            body = json_decode(self.request.body)
            email = body['email'].lower().strip()
            if not isinstance(email, str):
                raise Exception("Invalid email format")
            password = body['password']
            if not isinstance(password, str):
                raise Exception("Invalid password format")
        except Exception as e:
            logging.error(f"Input parsing error: {e}")
            self.send_error(400, message='You must provide an email address and password!')
            return

        if not email:
            self.send_error(400, message='The email address is invalid!')
            return

        if not password:
            self.send_error(400, message='The password is invalid!')
            return

        # Fetch the user from the database including salt and hashed password
        user = yield self.db.users.find_one({
            'email': email
        }, {
            'hashedpassword': 1,
            'salt': 1
        })

        if user is None:
            self.send_error(403, message='The email address and password are invalid!')
            return

        try:
            # Convert the salt from hex back to bytes
            salt = binascii.unhexlify(user['salt'])
            # Convert the stored hashed password from hex to bytes
            stored_hashed_password = binascii.unhexlify(user['hashedpassword'])

            # Set up Scrypt with the same parameters used during registration
            kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
            #added on 13/05/2025 at 00:25
            #PEPPER = "thebestpepper"
            #password = password + PEPPER 
            # Verify the entered password against the stored hashed password
            kdf.verify(password.encode('utf-8'), stored_hashed_password)
            logging.info("Password verification successful")

        except (InvalidKey, KeyError, binascii.Error) as e:
            logging.error(f"Password verification failed for email {email}: {e}")
            self.send_error(403, message='The email address and password are invalid!')
            return
        except Exception as e:
            logging.error(f"Unexpected error during password verification for {email}: {e}")
            self.send_error(500, message="Internal server error")
            return

        # Password verified successfully, generate a token
        try:
            token = yield self.generate_token(email)

            # If token generation failed, handle the error
            if token is None:
                logging.error("Token generation failed. Returning error response.")
                self.send_error(500, message="Internal server error during token response")
                return

            # Return the token
            self.set_status(200)
            self.response['token'] = token['token']
            self.response['expiresIn'] = token['expiresIn']
            self.write_json()

        except Exception as e:
            logging.error(f"Error while sending token response: {e}")
            self.send_error(500, message="Internal server error during token response")
            return
