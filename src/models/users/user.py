'''
__author__ = 'anis'
Date: 26.08.16
Time: 22:49
'''
import uuid

from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
import src.models.users.constants as UserConstants
from src.models.alerts.alert import Alert


class User(object):

    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an e-mail/password combo(as sent by the site forms) is valid or not.
        Checks that the e-mail exists, and password associated to that e-mail is correct.
        :param email: The user's email
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """
        user_data = Database.find_one(UserConstants.COLLECTION, query={"email": email})  # password in pbkdf2_sha512 format
        if user_data is None:
            # Users donot exists. Raise exception
            raise UserErrors.UserNotExistError("User name entered does not exist.")

        if not Utils.check_hashed_passwords(password, user_data['password']):
            # Tells that the password donot matches. Raise exception
            raise UserErrors.IncorrectPasswordError("Your password does not matches.")

        return True

    @staticmethod
    def register_user(email, password):
        """
        This methods registers a user using e-mail and password.
        The password already comes hashed as sha512.
        :param email: User's email
        :param password: sha512-hashed password
        :return: True if registered successfully, False otherwise
        """

        user_data = Database.find_one(UserConstants.COLLECTION, query={"email": email})
        if user_data is not None:
            # Tell user they already exist
            raise UserErrors.UserAlreadyRegisteredError("Email used to register already exists !")
        if not Utils.email_is_valid(email):
            # Tell user there email is not proper
            raise UserErrors.InvalidEmailError("The e-mail does not have the right format.")
        user = User(email, Utils.hash_password(password))
        user.save_to_db()

        return True

    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {"email": email}))

    def get_all_alerts(self):
        return Alert.find_by_user_email(self.email)
