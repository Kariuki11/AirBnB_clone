#!/usr/bin/python3
"""city class that inherits from BaseModel"""
from models.base_model import BaseModel


class City(BaseModel):
    """
    A City class for the AirBnB clone project.
    """

    state_id = ""  # Public class attribute: empty string for State.id
    name = ""
