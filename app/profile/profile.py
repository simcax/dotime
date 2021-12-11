'''Class to handle new users'''
from werkzeug.security import check_password_hash, generate_password_hash

class ProfileHandling:
    '''Profile handling'''

    @classmethod
    def create_password(cls,password):
        '''Generate password hash'''
        return generate_password_hash(password)

    @classmethod
    def validate_password(cls,password_hash, password):
        '''Check the password hash (from the database) can validate against the given password'''
        return check_password_hash(password_hash, password)
