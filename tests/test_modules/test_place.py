#!/usr/bin/python3
"""Defines unittests - models/place.py.

classes:
    TestPlace_instantiation
    TestPlace_save
    TestPlace_to_dict
"""
import unittest
import os
import models
import json
from datetime import datetime
from time import sleep
from models.place import Place


class FileStorage:
  """Serialize instances to JSON file and deserializes JSON file into instances."""

  __file_path = "file.json"  # Default file path
  __objects = {}  # Dictionary to store objects

  def _init_(self, file_path=None):
    """Initializes the FileStorage instance.

      Args:
          file_path (str, optional): The path to the JSON file. Defaults to "file.json".
      """
    if file_path:
      self.__file_path = file_path
    self.reload()

  def all(self):
    """Returns to a dictionary of all stored objects."""
    return self.__objects

  def new(self, obj):
    """Puts a new object to the storage."""
    key = f"{obj._class.name_}.{obj.id}"
    self.__objects[key] = obj

  def save(self):
    """Serializes all objects to JSON file."""
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
    """Deserializes JSON file to objects."""
    try:
      with open(self.__file_path, "r") as f:
        objdict = json.load(f)
        for key, value in objdict.items():
          self.new(eval(
              value["class"]))  # Assuming class the names are in the format "ClassName"
    except FileNotFoundError:
      pass  # Do nothing if the file doesn't exist


# Unittests for Place class (assuming Place is defined elsewhere)
import unittest
from models.place import Place  # Assuming place.py file is in models


class TestPlace_save(unittest.TestCase):
  """Unittests for testing save the method of Place class."""

  @classmethod
  def setUp(self):
    try:
      os.rename("file.json", "tmp")
    except IOError:
      pass

  def tearDown(self):
    try:
      os.remove("file.json")
    except IOError:
      pass
    try:
      os.rename("tmp", "file.json")
    except IOError:
      pass

  def test_one_save(self):
    pl = Place()
    sleep(0.05)
    first_updated_at = pl.updated_at
    pl.save()
    self.assertLess(first_updated_at, pl.updated_at)

  def test_two_saves(self):
    pl = Place()
    sleep(0.05)
    first_updated_at = pl.updated_at
    pl.save()
    second_updated_at = pl.updated_at
    self.assertLess(first_updated_at, second_updated_at)
    sleep(0.05)
    pl.save()
    self.assertLess(second_updated_at, pl.updated_at)

  def test_save_with_arg(self):
    pl = Place()
    with self.assertRaises(TypeError):
      pl.save(None)

  def test_save_updates_file(self):
    pl = Place()
    pl.save()
    plid = "Place." + pl.id
    with open("file.json", "r") as f:
      self.assertIn(plid, f.read())


class TestPlace_to_dict(unittest.TestCase):
  """Unittests for testing to_dict method of Place class."""

  def test_to_dict_type(self):
    self.assertTrue(dict, type(Place().to_dict()))

  def test_to_dict_contains_correct_keys(self):
    pl = Place()
    self.assertIn("id", pl.to_dict())
    self.assertIn("created_at", pl.to_dict())
    self.assertIn("updated_at", pl.to_dict())
    self.assertIn("_class_", pl.to_dict())

  def test_to_dict_contains_added_attributes(self):
    pl = Place()
    pl.middle_name = "Holberton"
    pl.my_number = 98
    self.assertEqual("Holberton", pl.middle_name)
    self.assertIn("my_number", pl.to_dict())

  def test_to_dict_datetime_attributes_are_strs(self):
    pl = Place()
    pl_dict = pl.to_dict()
    self.assertEqual(str, type(pl_dict["id"]))
    self.assertEqual(str, type(pl_dict["created_at"]))
    self.assertEqual(str, type(pl_dict["updated_at"]))

  def test_to_dict_output(self):
    dt = datetime.today()
    pl = Place()
    pl.id = "123456"
    pl.created_at = pl.updated_at = dt
    tdict = {
        'id': '123456',
        '_class_': 'Place',
        'created_at': dt.isoformat(),
        'updated_at': dt.isoformat(),
    }
    self.assertDictEqual(pl.to_dict(), tdict)

  def test_contrast_to_dict_dunder_dict(self):
    pl = Place()
    self.assertNotEqual(pl.to_dict(), pl._dict_)

  def test_to_dict_with_arg(self):
    pl = Place()
    with self.assertRaises(TypeError):
      pl.to_dict(None)


if __name__ == "__main__":
    unittest.main()