#!/usr/bin/env python3
"""
Obfuscates specified fields in a log message
using regex substitution.
"""

import re
from typing import List
import logging
import os
import mysql.connector
from mysql.connector import connection

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Obfuscates specified fields in a log message
    using regex substitution.
    """
    for field in fields:
        message = re.sub(f"{field}=[^{separator}]*",
                         f"{field}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records"""
        original_message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, original_message, self.SEPARATOR
        )


def get_logger() -> logging.Logger:
    """Returns a Logger object"""

    logger = logging.getLogger("user_date")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """
    Returns a connector to the database.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username, password=password, host=host, database=database
    )


def main():
    """
    Retrieves all rows in the users table and logs each row
    with filtered PII data.
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    for row in cursor:
        message = (
            f"name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]}; "
            f"password={row[4]}; ip={row[5]}; last_login={row[6]};user_agent={row[7]}"
        )
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
