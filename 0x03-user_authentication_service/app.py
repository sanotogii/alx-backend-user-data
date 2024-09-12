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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
