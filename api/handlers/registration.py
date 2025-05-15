from json import dumps
from logging import info
from tornado.escape import json_decode, utf8
from tornado.gen import coroutine
import os 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
#imported due to date of birth format on 21/04/2025 at 00:08
from datetime import datetime
#need to import config file here
#from conf import PEPPER
from ..conf import PEPPER #Relative import
from .base import BaseHandler



from .base import BaseHandler


class RegistrationHandler(BaseHandler):

    @coroutine
    def post(self):
        try:
            body = json_decode(self.request.body)
            email = body['email'].lower().strip()
            if not isinstance(email, str):
                raise Exception()
            password = body['password']
            if not isinstance(password, str):
                raise Exception()
            display_name = body.get('displayName')
            if display_name is None:
                display_name = email
            if not isinstance(display_name, str):
                raise Exception()
            # phone number added 
            phone_number = body.get('phonenumber')
            if not isinstance(phone_number, int):
                raise Exception()
            #address added 
            address = body.get('address')
            if not isinstance(address, str):
                raise Exception()
            #full name added on 21/04/2025 at 23:43
            full_name = body.get('fullname')
            if not isinstance(full_name, str):
                raise Exception()
            #disabilities added on 13/05/2025 at 18:32
            disabilities = body.get('disabilities')
            if not isinstance(disabilities, str):
                raise Exception()
            #date of birth added on 21/04/2025 at 23:43
            date_of_birth = body.get('dateofbirth')
            if not isinstance(date_of_birth, str):
                raise Exception()
            
            #added on 23/04/2025 at 18:36 , a field name hashed_password is added
            hashed_password = body.get('hashedpassword')
            if not isinstance(date_of_birth, str):
                raise Exception()
            
            """
            #nonce value is added on 20/04/2025 at 00:25
            nonce = body.get('nonce')
            if not isinstance(nonce, str):
                raise Exception()
            """
            
        except Exception as e:
            self.send_error(400, message='You must provide an email address, password and display name!')
            return

        if not email:
            self.send_error(400, message='The email address is invalid!')
            return

        if not password:
            self.send_error(400, message='The password is invalid!')
            return

        if not display_name:
            self.send_error(400, message='The display name is invalid!')
            return
        # phone number added
        if not phone_number:
            self.send_error(400, message='The phone number is invalid!')
            return
        # address added
        if not address:
            self.send_error(400, message='The address is invalid!')
            return
        # full name added on 21/04/2025 at 23:43
        if not full_name:
            self.send_error(400, message='The full name is invalid!')
            return
        # disabilities added on 13/05/2025 at 18:32
        if not disabilities:
            self.send_error(400, message='The disabilities is invalid!')
            return
        # date of birth added on 21/04/2025 at 23:43
        if not date_of_birth:
            self.send_error(400, message='The date of birth is invalid!')
            return
       
        #validate the date format for date of birth
        """
        try:
            dob = datetime.strptime(date_of_birth, '%Y-%m-%d')
        except ValueError:
            self.send_error(400, message='The date of birth format is invalid! Use YYYY-MM-DD')
            return
        """
        #ends here

        user = yield self.db.users.find_one({
          'email': email
        }, {})

        if user is not None:
            self.send_error(409, message='A user with the given email address already exists!')
            return
        
        # perform the encrypt for the personal details
        
        # Encrypt the plaintext using ChaCha20
        key = "thebestsecretkeyintheentireworld"
        key_bytes = bytes(key, "utf-8")
        print("Key: " + key)

        nonce_bytes = os.urandom(16)
        chacha20_cipher = Cipher(algorithms.ChaCha20(key_bytes, nonce_bytes), 
                        mode=None)
        #lines added on 20/04/2025 at 13:37
        #nonce_bytes = bytes(nonce, "utf-8")
        print("Nonce: " + nonce_bytes.hex())
        nonce_bytes_hex = nonce_bytes.hex()
        

        chacha20_encryptor = chacha20_cipher.encryptor()
        #added on 20/04/2025 at 18:40
        chacha20_decryptor = chacha20_cipher.decryptor()
        plaintext = "someemail"
        plaintext_bytes = bytes(plaintext, "utf-8")
        print("Plaintext: " + plaintext)

        ciphertext_bytes = chacha20_encryptor.update(email.encode())
        encrypted_email = ciphertext_bytes.hex()
        #added code for dectypting the personal details on 20/04/2025 at 18:39
        decrypted_email = chacha20_decryptor.update(ciphertext_bytes)

        ciphertext_bytes_displayname = chacha20_encryptor.update(display_name.encode())
        encrypted_display_name = ciphertext_bytes_displayname.hex()
        #added code for dectypting the personal details on 20/04/2025 at 18:39
        decrypted_display_name = chacha20_decryptor.update(ciphertext_bytes_displayname)
        
        phone_bytes = phone_number.to_bytes(4, byteorder='big')
        ciphertext_bytes_phonenumber = chacha20_encryptor.update(phone_bytes)
        encrypted_phonenumber = ciphertext_bytes_phonenumber.hex()
        #added code for dectypting the personal details on 20/04/2025 at 18:41
        decrypted_phonenumber = chacha20_decryptor.update(ciphertext_bytes_phonenumber)
        """
        ciphertext_bytes_phonenumber = chacha20_encryptor.update(phone_number.encode())
        encrypted_phonenumber = ciphertext_bytes_phonenumber.hex()
        """
        ciphertext_bytes_address = chacha20_encryptor.update(address.encode())
        encrypted_address = ciphertext_bytes_address.hex()
        #added code for dectypting the personal details on 20/04/2025 at 18:41
        decrypted_address = chacha20_decryptor.update(ciphertext_bytes_address)

        #added code for dectypting the personal details on 21/04/2025 at 23:49
        ciphertext_bytes_fullname = chacha20_encryptor.update(full_name.encode())
        encrypted_fullname = ciphertext_bytes_fullname.hex()
        decrypted_fullname = chacha20_decryptor.update(ciphertext_bytes_fullname)

        #added disabilities on 13/05/2025 at 18:32
        ciphertext_bytes_disabilities = chacha20_encryptor.update(disabilities.encode())
        encrypted_disabilities = ciphertext_bytes_disabilities.hex()
        decrypted_disabilities = chacha20_decryptor.update(ciphertext_bytes_disabilities)
        
        ciphertext_bytes_dateofbirth = chacha20_encryptor.update(date_of_birth.encode())
        encrypted_dateofbirth = ciphertext_bytes_dateofbirth.hex()
        decrypted_dateofbirth = chacha20_decryptor.update(ciphertext_bytes_dateofbirth)


        

        print("Ciphertext: " + encrypted_email)

       
    

        #ends here
        
        
        # hash the password

        #starts here
        salt = os.urandom(16)#generated on per user basis
        #pepper = os.urandom(16)#pepper is added as per our practical on 21/04/2025 at 01:26 generated per application basis
        #PEPPER = "thebestpepper"
        #kdf = Scrypt(salt = salt + PEPPER, length=32, n=2**14, r=8, p=1)
        kdf = Scrypt(salt=salt + PEPPER, length=32, n=2**14, r=8, p=1)
        
        #password = password + PEPPER
        
        #password = input("Please enter your password: ")
        password_bytes = bytes(password, "utf-8")
        hashed_password = kdf.derive(password_bytes)
        #added 20/11/2025 at 15:29
        salt_hex = salt.hex()

        print("Algorithm: Scrypt")
        print("Salt: " + salt.hex())
        print("Length: 32")
        print("n: 2**14")
        print("r: 8")
        print("p: 1")
        hashed_password_hex_format = hashed_password.hex()
        print("Hashed password: " + hashed_password.hex())
        #ends here
        
        yield self.db.users.insert_one({
             #'email': encrypted_email,#added for encrypted email
            #nonce value is added on 20/04/2025 at 00:25
            'nonce': nonce_bytes_hex,
            #salt value is added on 20/11/2025 at 15:30
            'salt': salt_hex,
            'email': email,
            #'password': password, # the password is stored in the clear!
            'hashedpassword': hashed_password_hex_format, # the hashed password is stored in the clear!#added on 23/04/2025 at 18:39
            #'password': hashed_password,
            #'displayName': display_name, # the personal details are stored in the clear!
            'displayName': encrypted_display_name,
            #added on 13/05/2025 at 3 PM ,will work from here
            # storing in db for retrieve for decryption process in user.py
            #'phonenumber': phone_number, # phone number added
            'phonenumber': encrypted_phonenumber,
            #'address': address           # address added
            'address': encrypted_address,
            #added on 21/04/2025 at 23:43
            'fullname': encrypted_fullname,
            'disabilities': encrypted_disabilities,
            'dateofbirth': encrypted_dateofbirth,
         
            
        })

        self.set_status(200)
        self.response['email'] = email
        #nonce value is added on 20/04/2025 at 00:25
        self.response['nonce'] = nonce_bytes_hex #added 20/04/2025 at 14:06
        #salt value is added on 20/11/2025 at 15:30
        #self.response['salt'] = salt_hex
        self.response['displayName'] = display_name
        self.response['phonenumber'] = phone_number
        self.response['address'] = address
        self.response['fullname'] = full_name
        self.response['disabilities'] = disabilities
        self.response['dateofbirth'] = date_of_birth
       

        self.write_json()
    
 
         