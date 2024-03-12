#!/usr/bin/python3
from models.base_model import BaseModel
"""It creates a User class that inherits from BaseModel"""


class User(BaseModel):
    """
    A User class for the AirBnB clone project.
    """

    email = ""  # Public class attribute: empty string
    password = ""  # Public class attribute: empty string
    first_name = ""  # Public class attribute: empty string
    last_name = ""  # Public class attribute: empty string
