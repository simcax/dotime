"""Class to contain common testing utility methods"""

import random
import string


class TestUtils:
    """The test utility class"""

    @classmethod
    def createRandomString(cls):
        """'Helper function to create a random string - 10 chars long"""
        randomString = "".join(random.choice(string.ascii_letters) for x in range(10))
        return randomString

    def createRandomEmail(self):
        """Helper function to create a random email address"""
        firstpart = self.createRandomString()
        email = f"{firstpart}@dotime.me"
        return email
