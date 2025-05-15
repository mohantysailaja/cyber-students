from datetime import datetime
from time import mktime
from tornado.gen import coroutine

from .base import BaseHandler



class AuthHandler(BaseHandler):

    @coroutine
    def prepare(self):
        super(AuthHandler, self).prepare()

        if self.request.method == 'OPTIONS':
            return

        try:
            token = self.request.headers.get('X-Token')
            if not token:
              raise Exception()
        except:
            self.current_user = None
            self.send_error(400, message='You must provide a token!')
            return

        user = yield self.db.users.find_one({
            'token': token
        }, {
            'email': 1,
            'nonce': 1,
            'displayName': 1,
            'phonenumber': 1,
            'address': 1,
            'dateofbirth': 1,
            'fullname': 1,
            'disabilities': 1,
            'expiresIn': 1
        })

        if user is None:
            self.current_user = None
            self.send_error(403, message='Your token is invalid!')
            return

        current_time = mktime(datetime.now().utctimetuple())
        if current_time > user['expiresIn']:
            self.current_user = None
            self.send_error(403, message='Your token has expired!')
            return

        self.current_user = {
            'email': user['email'],
            'nonce': user['nonce'], # nonce value is added on 20/04/2025 at 00:25
            'display_name': user['displayName'],
            'phone_number': user['phonenumber'],
            'address': user['address'],
            'date_of_birth': user['dateofbirth'],#added on 21/04/2025 at 23:47
            'full_name': user['fullname'],
            'disabilities': user['disabilities']#added on 13/5/2025
        }

        
        #code added for decryption on 25/04/2025 at 2:16AM 

        