#!/usr/bin/env python3
"""
BasicAuth Class that inherits from Auth
"""
from .auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """BasicAuth class that inherits from Auth"""

    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        """
        Extracts the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split("Basic ", 1)[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        Decodes the Base64 part of the Authorization header
        for Basic Authentication.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header,
                                             validate=True)
            return decoded_bytes.decode("utf-8")
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        Extracts the user email and password from the
        Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """
        Returns the User instance based on email and password.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})
        if not users:
            return None

        user = users[0]

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar("User"):
        """
        Retrieves the User instance for a request using
        Basic Authentication.
        """
        # Get the Authorization header from the request
        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None

        # Extract the Base64 part of the Authorization header
        base64_authorization = self.extract_base64_authorization_header(
            authorization_header
        )
        if base64_authorization is None:
            return None

        # Decode the Base64 part of the Authorization header
        decoded_authorization = self.decode_base64_authorization_header(
            base64_authorization
        )
        if decoded_authorization is None:
            return None

        # Extract user credentials from the decoded Authorization header
        user_email, user_pwd = self.extract_user_credentials(
            decoded_authorization)
        if user_email is None or user_pwd is None:
            return None

        # Retrieve the User object from the credentials
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
