# 0x03. User Authentication Service

## Project Overview
This project focuses on implementing a user authentication service using Python, Flask, and SQLAlchemy. The goal is to create a robust system that handles user registration, login, session management, and password reset functionalities.

## Project Details
- **Back-end**
- **Authentication**
- **Weight:** 1

## Learning Objectives
By the end of this project, you should be able to explain:

- How to declare API routes in a Flask app
- How to get and set cookies
- How to retrieve request form data
- How to return various HTTP status codes

## Requirements
- Allowed editors: vi, vim, emacs
- All files interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)
- All files should end with a new line
- The first line of all files should be exactly `#!/usr/bin/env python3`
- A `README.md` file, at the root of the project folder, is mandatory
- Code should use the pycodestyle style (version 2.5)
- SQLAlchemy 1.3.x should be used
- All files must be executable
- The length of files will be tested using `wc`
- All modules, classes, and functions should have documentation
- All functions should be type annotated
- The flask app should only interact with `Auth` and never with `DB` directly
- Only public methods of `Auth` and `DB` should be used outside these classes

## Setup
Install bcrypt:
```
pip3 install bcrypt
```

## Tasks
The project is divided into several tasks, each focusing on a specific aspect of the authentication service. Some key tasks include:

1. Creating a User model
2. Implementing user registration
3. Implementing credential validation
4. Generating session IDs
5. Implementing login and logout functionality
6. Creating a user profile endpoint
7. Implementing password reset functionality

## Files
- `user.py`: Defines the User model
- `db.py`: Handles database operations
- `auth.py`: Implements authentication logic
- `app.py`: Contains the Flask application and routes

## Testing
An end-to-end integration test is provided in `main.py`. Run it to validate the entire authentication flow.

## Author
Khalid LAZRAG

## Acknowledgements
This project is part of the ALX Backend SE curriculum.
