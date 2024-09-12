#!/usr/bin/env python3
import requests

BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """
    Register a new user.
    """
    res = requests.post(
        f"{BASE_URL}/users", data={"email": email, "password": password}
    )
    assert (
        res.status_code == 200
    ), f"Expected status code 200, but got {res.status_code}"
    assert res.json() == {
        "email": email,
        "message": "user created",
    }, f"Unexpected response: {res.json()}"


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempt to log in with the wrong password.
    """
    res = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password}
    )
    assert (
        res.status_code == 401
    ), f"Expected status code 401, but got {res.status_code}"


def log_in(email: str, password: str) -> str:
    """
    Log in with correct credentials.
    Returns the session ID.
    """
    res = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password}
    )
    assert (
        res.status_code == 200
    ), f"Expected status code 200, but got {res.status_code}"
    session_id = res.cookies.get("session_id")
    assert session_id is not None, "No session_id in cookies"
    return session_id


def profile_unlogged() -> None:
    """
    Access profile without being logged in.
    """
    res = requests.get(f"{BASE_URL}/profile")
    assert (
        res.status_code == 403
    ), f"Expected status code 403, but got {res.status_code}"


def profile_logged(session_id: str) -> None:
    """
    Access profile while logged in.
    """
    res = requests.get(f"{BASE_URL}/profile",
                       cookies={"session_id": session_id})
    assert (
        res.status_code == 200
    ), f"Expected status code 200, but got {res.status_code}"
    assert "email" in res.json(), "No email in profile response"


def log_out(session_id: str) -> None:
    """
    Log out the user.
    """
    res = requests.delete(f"{BASE_URL}/sessions",
                          cookies={"session_id": session_id})
    assert (
        res.status_code == 200
    ), f"Expected status code 200, but got {res.status_code}"


def reset_password_token(email: str) -> str:
    """
    Request a reset password token.
    """
    res = requests.post(f"{BASE_URL}/reset_password", data={"email": email})
    assert (
        res.status_code == 200
    ), f"Expected status code 200, but got {res.status_code}"
    reset_token = res.json().get("reset_token")
    assert reset_token is not None, "No reset_token in response"
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update the user's password using the reset token.
    """
    res = requests.put(
        f"{BASE_URL}/reset_password",
        data={"email": email, "reset_token": reset_token,
              "new_password": new_password},
    )
    assert (
        res.status_code == 200
    ), f"Expected status code 200, but got {res.status_code}"
    assert res.json() == {
        "email": email,
        "message": "Password updated",
    }, f"Unexpected response: {res.json()}"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
