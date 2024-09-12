#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request, Response
from auth import Auth
from typing import Dict, Any

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def Bonjour():
    """
    Basic Flask app
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> Response:
    """
    POST /users endpoint to register a user.
    """

    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
