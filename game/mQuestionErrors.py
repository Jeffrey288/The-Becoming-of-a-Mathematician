"""
mQuestionErrors.py
"""

class Error(Exception):

    def __init__(self, message):
        self.message = message

class FractionError(Error):

    def __init__(self, message = "Fraction too large. Regeneration is required."):
        self.message = message

class RangeError(Error):

    def __init__(self, message):
        self.message = message

class ArrayError(Error):

    def __init__(self):
        self.message = "Attribute range not wide enough to produce specified number of objects."

class TypeError(Error):

    def __init__(self, message):
        self.message = message

class ValidationError(Error):

    def __init__(self, message = "The generated variables have failed validation. Regeneration is requried."):
        self.message = message