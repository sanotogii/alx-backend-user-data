#!/usr/bin/env python3
"""
This module provides authentication-related utilities.
"""
import bcrypt
from db import DB, NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        bytes: The hashed password.
    """
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the provided email and password.

        Args:
            email (str): The email address of the user to register.
            password (str): The plaintext password of the user to register.

        Returns:
            User: The newly created user object.

        Raises:
            ValueError: If a user with the provided email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pw = _hash_password(password)
            user = self._db.add_user(email, hashed_pw)

            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates user login credentials.

        Args:
            email (str): The email of the user.
            password (str): The plain text password to check.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)

            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except NoResultFound:
            return False

        return False
