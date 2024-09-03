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

        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        if path.endswith('/'):
            normalized_path = path
        else:
            normalized_path = path + '/'

        if normalized_path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """Returns None - to be implemented later."""
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Returns None - to be implemented later."""
        return None
