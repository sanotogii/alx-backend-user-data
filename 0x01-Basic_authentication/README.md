# Basic Authentication API

## Project Overview

In this project, you will gain a deep understanding of the authentication process by implementing Basic Authentication on a simple API. While it is recommended to use existing modules or frameworks like `Flask-HTTPAuth` for authentication in production environments, this project is designed for educational purposes. You will implement each step of the Basic Authentication mechanism to understand its inner workings.

## Learning Objectives

By the end of this project, you will be able to explain the following concepts:

- **Authentication:** The process of verifying the identity of a user.
- **Base64 Encoding:** A method to encode binary data into ASCII characters.
- **Basic Authentication:** A simple authentication method that involves encoding credentials using Base64.
- **Authorization Header:** The HTTP header used to transmit credentials in Basic Authentication.

## Requirements

- **Python Version:** Python 3.7
- **Operating System:** Ubuntu 18.04 LTS
- **Style Guide:** PEP 8 (pycodestyle 2.5)
- **Documentation:** All modules, classes, and functions must include docstrings.

## Setup Instructions

1. **Install Dependencies:**

   ```bash
   pip3 install -r requirements.txt
   ```

2. **Run the API Server:**

   ```bash
   API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
   ```

3. **Test the API:**

   ```bash
   curl "http://0.0.0.0:5000/api/v1/status" -vvv
   ```

## Project Structure

- **Simple-basic-API:** Setup a basic API with a `User` model, where users are stored via serialization/deserialization in files.
- **Error Handlers:**
  - **401 Unauthorized:** Handle unauthorized requests with a JSON response `{"error": "Unauthorized"}`.
  - **403 Forbidden:** Handle forbidden requests with a JSON response `{"error": "Forbidden"}`.
- **Auth Class:** A template class for managing API authentication.
- **BasicAuth Class:** A class that inherits from `Auth` to implement Basic Authentication.
- **Authorization Header:** Implement the mechanism to validate and extract credentials from the Authorization header.

## Key Tasks

1. **Setup API Server:**
   - Start the server and test basic API functionality.
   
2. **Error Handling:**
   - Implement handlers for `401 Unauthorized` and `403 Forbidden` errors.

3. **Auth Class:**
   - Create a base class to manage API authentication.
   - Implement methods to validate requests and handle authorization headers.

4. **BasicAuth Class:**
   - Implement Basic Authentication by inheriting from the `Auth` class.
   - Extract and decode Base64 credentials from the Authorization header.

## Usage Example

After starting the API server, you can interact with it using `curl`:

- **Check API Status:**
  
  ```bash
  curl "http://0.0.0.0:5000/api/v1/status"
  ```

- **Unauthorized Access:**
  
  ```bash
  curl "http://0.0.0.0:5000/api/v1/users"
  # Response: {"error": "Unauthorized"}
  ```

- **Forbidden Access:**
  
  ```bash
  curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Test"
  # Response: {"error": "Forbidden"}
  ```

## Repository

- **GitHub Repository:** `alx-backend-user-data`
- **Directory:** `0x01-Basic_authentication`

## Author

This project is part of the curriculum for the ALX Backend program. It is designed to provide hands-on experience with authentication mechanisms in web APIs.
