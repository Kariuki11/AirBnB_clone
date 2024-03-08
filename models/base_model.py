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
    if kwargs is not None and kwargs != {}:  # Existing object with attributes
      self.id = kwargs.get("id")
      if self.id is None:  # Assign ID if not already present
          self.id = str(uuid.uuid4())

      self.created_at = datetime.strptime(kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
      self.updated_at = datetime.strptime(kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")

      for key, value in kwargs.items():
          if key not in ["id", "created_at", "updated_at", "_class_"]:
              setattr(self, key, value)
    else:  # New object
      self.id = str(uuid.uuid4())
      self.created_at = self.updated_at = datetime.now()
      self.id = str(uuid.uuid4())  # Generate unique ID as string
      self.created_at = datetime.utcnow()  # Current datetime at creation
      self.updated_at = self.created_at  # Update time initially same as creation

  def _str_(self):
    """
    String representation of the object.
    """
    return f"[{self._class.name}] ({self.id}) {self.dict_}"

  def save(self):
    """Updates the updated_at quality with the current datetime and possibly saves the item."""
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