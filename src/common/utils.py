'''
__author__ = 'anis'
Date: 26.08.16
Time: 22:48
'''
import re
from passlib.hash import pbkdf2_sha512


class Utils(object):

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[\w.-]+@([\w]+\.)+[\w]+$')  # anis-cuet016@gmail.com.bd
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: The sha512 password from login/register form
        :return: A sha512->pbkdf2_sha512 encrypted password
        """

        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_passwords(password, hashed_password):
        """
        Checks whether the password user sent matches with that of database.
        :param password: user sending this password in sha512 encrypted form
        :param hashed_password: pbkdf2_sha412 encrypted password in the database
        :return: True if matched, False otherwise
        """

        return pbkdf2_sha512.verify(password, hashed_password)