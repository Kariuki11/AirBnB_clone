#!/usr/bin/python3
"""It creates a place class that inherits from BaseModel"""
from models.base_model import BaseModel


class Place(BaseModel):
    """
  A Spot class for the AirBnB clone project.
    """

    city_id = ""  # Public class attribute: empty string for City.id
    user_id = ""  # Public class attribute: empty string for User.id
    name = ""  # Public class attribute: empty string
    description = ""  # Public class attribute: empty string
    number_rooms = 0  # Public class attribute: default 0
    number_bathrooms = 0  # Public class attribute: default 0
    max_guest = 0  # Public class attribute: default 0
    price_by_night = 0  # Public class attribute: default 0
    latitude = 0.0  # Public class attribute: default 0.0
    longitude = 0.0  # Public class attribute: default 0.0
    amenity_ids = []  # Public class attribute: empty list for Amenity.id
