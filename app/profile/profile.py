'''Class to handle new users'''
from werkzeug.security import check_password_hash, generate_password_hash

class ProfileHandling:
    '''Profile handling'''

    def create_password(self,password):
        '''Generate password hash'''
        return generate_password_hash(password)
