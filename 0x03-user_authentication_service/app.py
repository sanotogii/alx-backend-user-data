#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request, Response, make_response, abort
from flask import redirect
from auth import Auth
from typing import Dict, Any


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def Bonjour():
    """
    Basic Flask app
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """
    POST /users endpoint to register a user.
    """

    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """
    POST /sessions endpoint for user login.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    # Validate login credentials
    if not AUTH.valid_login(email, password):
        abort(401)

    # Create session ID and set it as a cookie
    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """
    DELETE /sessions endpoint to log out a user.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect("/")


@app.route("/profile", methods=["GET"])
def profile():
    """
    GET /profile endpoint to get user profile.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"])
def reset_password():
    """
    POST /reset_password endpoint to generate a
    reset password token.
    """
    email = request.form.get("email")

    if not email:
        abort(400, description="Email is required")

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403, description="Email not found")


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """
    PUT /reset_password endpoint to update a user's password.

    Expects form data with 'email', 'reset_token', and 'new_password'.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    if not email or not reset_token or not new_password:
        abort(400)

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
