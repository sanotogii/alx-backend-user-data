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
