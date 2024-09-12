#!/usr/bin/env python3
"""
This module provides authentication-related utilities.
"""
import bcrypt


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
