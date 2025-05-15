from tornado.web import authenticated

from .auth import AuthHandler

class UserHandler(AuthHandler):

    @authenticated
    def get(self):
        # decrypt the display_name
        #decrypted_display_name = self.decrypt(self.current_user['display_name'])
        #self.current_user['display_name'] = decrypted_display_name
        
        
        self.set_status(200)
        #
       
        self.response['email'] = self.current_user['email']
        #nonce value is added on 20/04/2025 at 00:25
        self.response['nonce'] = self.current_user['nonce']
        self.response['displayName'] = self.current_user['display_name']
        #self.response['displayName'] = decrypted_display_name
        #code added for phone number and address
        self.response['phonenumber'] = self.current_user['phone_number']
        self.response['address'] = self.current_user['address']
        #code added for full name and date of birth
        self.response['fullname'] = self.current_user['full_name']
        self.response['disabilities'] = self.current_user['disabilities'] #added on 13/5/2025
        self.response['dateofbirth'] = self.current_user['date_of_birth']

        #decrypted personal details
        #self.response['displayName_decypted'] = self.current_user['display_name'].decrypt()
       
        #code added for decryption on 25/04/2025 at 2:16AM
         # decrypt the display name using ChaCha20 at 2:35
       
        #decrypted_display_name = self.decrypt(self.current_user['display_name'])
        #self.response['displayName'] = decrypted_display_name   
        #displaying decrypted records starts here 

        #decryption code
        
        
        #ends here
        
        
        #ends here
        self.write_json()
       

       