#!/usr/bin/env python3
"""
auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class template for managing API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False, indicating that no authentication is required."""

        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        if not path.endswith('/'):
            path = path + '/'

        for excluded_path in excluded_paths:
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Returns None - to be implemented later."""
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar("User"):
        """Returns None - to be implemented later."""
        return None
