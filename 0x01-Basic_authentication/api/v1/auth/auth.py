#!/usr/bin/env python3
from flask import request
from typing import List, TypeVar

"""
auth class
"""


class Auth:
    """Auth class template for managing API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False, indicating that no authentication is required."""
        return False

    def authorization_header(self, request=None) -> str:
        """Returns None - to be implemented later."""
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Returns None - to be implemented later."""
        return None
