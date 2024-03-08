#!/usr/bin/python3
"""It creates an Amenity class that inherits from Basic model."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    An Amenity class for the AirBnB clone project.
    """

    name = ""