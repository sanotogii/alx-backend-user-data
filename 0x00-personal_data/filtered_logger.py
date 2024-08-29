#!/usr/bin/env python3
"""
Regex-ing
"""

import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscates specified fields in a log message
    using regex substitution.
    """
    for field in fields:
        message = re.sub(f'{field}=[^{separator}]*', f'{field}={redaction}', message)
    return message
