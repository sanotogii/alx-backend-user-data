#!/usr/bin/env python3
"""
Hash a password string using bcrypt and return
the salted, hashed password.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password string using bcrypt and return
    the salted, hashed password.
    """
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed = bcrypt.hashpw(password.encode(), salt)

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if the provided password matches the hashed password.
    """
    # Use bcrypt to compare the provided password with the hashed password
    isValid = bcrypt.checkpw(password.encode(), hashed_password)
    return isValid
