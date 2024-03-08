#!/usr/bin/python3
"""Defines the file storage class."""

import json
from datetime import datetime  # Optional for future timestamps

class FileStorage:
  """Serialize instances to a JSON file and deserializes JSON file to instances."""

  __file_path = "file.json"  # Default file path
  __objects = {}  # Dictionary to store objects

  def _init_(self, file_path=None):
    """Initialize the FileStorage instance.

    Args:
      file_path (str, optional): The path to the JSON file. Defaults to "file.json".
    """
    if file_path:
      self.__file_path = file_path
    self.reload()

  def all(self):
    """Returns dictionary of all stored objects."""
    return self.__objects

  def new(self, obj):
    """Add another item to the storage."""
    key = f"{obj._class.name_}.{obj.id}"
    self.__objects[key] = obj

  def save(self):
    """Serializes all objects to the JSON file."""
    try:
      # Include timestamps in serialized data (optional)
      objdict = {key: value.to_dict() for key, value in self.__objects.items()}
      for obj in objdict.values():
        obj['updated_at'] = datetime.utcnow().isoformat()
      with open(self.__file_path, "w") as f:
        json.dump(objdict, f)
    except Exception as e:
      print(f"Error saving to file: {e}")

  def reload(self):
    """Deserializes the JSON file to objects."""
    try:
      with open(self.__file_path, "r") as f:
        objdict = json.load(f)
        for key, value in objdict.items():
          pass
    except FileNotFoundError:
      pass  # Do nothing if the file doesn't exist