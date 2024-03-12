#!/usr/bin/python3
import uuid
from datetime import datetime
from models import storage


class BaseModel:

    """
  A base class for different models.
  """

    def _init_(self, *args, **kwargs):
    """The _init_ initializes objects when they are created.

  self: Addresses the case of the class
  *args and **kwargs: Allow passing variable numbers of arguments.
    """
    if kwargs is not None and kwargs != {}:
        self.id = kwargs.get("id")
    if self.id is None:  
        self.id = str(uuid.uuid4())

        self.created_at = parse_datetime(kwargs.get("created_at"))
        self.updated_at = parse_datetime(kwargs.get("updated_at", self.created_at.isoformat()))
    for key, value in kwargs.items():
    if key not in ["id", "created_at", "updated_at", "_class_"]:
                    setattr(self, key, value)
    else:
        self.id = str(uuid.uuid4())
        self.created_at = self.updated_at = datetime.now()
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def _str_(self):
        """
    String representation of the object.
    """
    return f"[{self._class.name}] ({self.id}) {self.dict_}"

    def save(self):
        """Updates updated_at quality with current datetime and possibly saves item."""
        self.updated_at = datetime.now()

    def to_dict(self):
    """
    Provides a dictionary representation of the object.
    """
    my_dict = self._dict_.copy()
    my_dict["_class"] = self._class.name
    my_dict["created_at"] = self.created_at.isoformat()
    my_dict["updated_at"] = self.updated_at.isoformat()
    return my_dict
