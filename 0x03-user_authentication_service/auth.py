#!/usr/bin/env python3
"""
This module provides authentication-related utilities.
"""
import bcrypt
from db import DB, NoResultFound
from user import User
import uuid
from typing import Union
from uuid import uuid4


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


def _generate_uuid() -> str:
    """
    Generate a new UUID.

    Returns:
        str: String representation of a new UUID.
    """
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> Union[str, None]:
        """
        Create a new session for the user and return
        the session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Retrieves a user by their session ID.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a session for a user given the user's ID.

        Args:
            user_id (int): The ID of the user whose session is to be
            destroyed.
        """
        if user_id is None:
            return None

        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token for the user with the given email.

        Args:
            email (str): The email of the user requesting a password reset.

        Returns:
            str: The generated reset password token.

        Raises:
            ValueError: If no user is found with the provided email.
        """
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError("User not found")

        reset_token = str(uuid4())

        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update the user's password using the reset token.
        Args:
            reset_token (str): The reset token for identifying the user.
            password (str): The new password to set.
        Raises:
            ValueError: If the reset_token is invalid or not found.
        """
        user = self._db.find_user_by(reset_token=reset_token)
        if not user:
            raise ValueError("Invalid reset token")

        hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                        bcrypt.gensalt())

        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update the user's password using the reset token.

        Args:
            reset_token (str): The reset token for identifying the user.
            password (str): The new password to set.

        Raises:
            ValueError: If the reset_token is invalid or not found.
        """
        user = self._db.find_user_by(reset_token=reset_token)

        if not user:
            raise ValueError("Invalid reset token")

        hashed_password = _hash_password(password)

        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)
