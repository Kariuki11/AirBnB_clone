#!/usr/bin/python3
"""It creates a State class that inherits from BaseModel"""
from models.base_model import BaseModel


class State(BaseModel):
    """
    State class for the AirBnB clone project.
    """

    name = ""  # Public class attribute: empty string
