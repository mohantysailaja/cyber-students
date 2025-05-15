from json import dumps
from tornado.escape import json_decode
from tornado.ioloop import IOLoop
from tornado.web import Application
import os 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

from api.handlers.registration import RegistrationHandler

from .base import BaseTest

import urllib.parse

class RegistrationHandlerTest(BaseTest):

    @classmethod
    def setUpClass(self):
        self.my_app = Application([(r'/registration', RegistrationHandler)])
        super().setUpClass()

    def test_registration(self):
        email = 'test@test.com'
        display_name = 'testDisplayName'
        

        body = {
          'email': email,
          'password': 'testPassword',
          'displayName': display_name,
          'phoneNumber': '1234567890',
          'address': '123 Test St',
          'dateOfBirth': '2000-01-01',
          'fullName': 'Test User',
          'disabilities': 'None'
        }

        response = self.fetch('/registration', method='POST', body=dumps(body))
        self.assertEqual(200, response.code)

        body_2 = json_decode(response.body)
        self.assertEqual(email, body_2['email'])
        self.assertEqual(display_name, body_2['displayName'])
        self.assertEqual(body['phoneNumber'], body_2['phoneNumber'])
        self.assertEqual(body['address'], body_2['address'])
        self.assertEqual(body['dateOfBirth'], body_2['dateOfBirth'])
        self.assertEqual(body['fullName'], body_2['fullName'])
        self.assertEqual(body['disabilities'], body_2['disabilities'])


    def test_registration_without_display_name(self):
        email = 'test@test.com'

        body = {
          'email': email,
          'password': 'testPassword'
        }

        response = self.fetch('/registration', method='POST', body=dumps(body))
        self.assertEqual(200, response.code)

        body_2 = json_decode(response.body)
        self.assertEqual(email, body_2['email'])
        self.assertEqual(email, body_2['displayName'])
        self.assertEqual(body['phoneNumber'], body_2['phoneNumber'])
        self.assertEqual(body['address'], body_2['address'])
        self.assertEqual(body['dateOfBirth'], body_2['dateOfBirth'])
        self.assertEqual(body['fullName'], body_2['fullName'])
        self.assertEqual(body['disabilities'], body_2['disabilities'])


     # decrypt the plaintext using ChaCha20
        """
        key = "thebestsecretkeyintheentireworld"
        key_bytes = bytes(key, "utf-8")
        print("Key: " + key)

        nonce_bytes = os.urandom(16)
        def decrypt(self,encrypted_data):
            cipher = Cipher(algorithms.ChaCha20(key_bytes, nonce_bytes), 
                            mode=None)
            decryptor = cipher.decryptor()
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
            return decrypted_data.decode()
        
        
        #ends here
        """
    
    def test_registration_twice(self):
        body = {
          'email': 'test@test.com',
          'password': 'testPassword',
          'displayName': 'testDisplayName',
          'phoneNumber': '1234567890',
          'address': '123 Test St',
          'dateOfBirth': '2000-01-01',
          'fullName': 'Test User',
          'disabilities': 'None'
        }

        response = self.fetch('/registration', method='POST', body=dumps(body))
        self.assertEqual(200, response.code)

        response_2 = self.fetch('/registration', method='POST', body=dumps(body))
        self.assertEqual(409, response_2.code)
