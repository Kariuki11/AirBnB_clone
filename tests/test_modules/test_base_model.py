import unittest
from models.base_model import BaseModel
from datetime import datetime
import os 
from time import sleep
import models

class TestBaseModel(unittest.TestCase):
  """Unittests for testing the BaseModel class."""

  def test_id_is_public_str(self):
    """Test that id attribute is a string and unique."""
    bm1 = BaseModel()
    bm2 = BaseModel()
    self.assertEqual(str, type(bm1.id))
    self.assertNotEqual(bm1.id, bm2.id)

  def test_created_at_is_public_datetime(self):
    """Test that create_at attribute is datetime object."""
    bm = BaseModel()
    self.assertEqual(datetime, type(bm.created_at))

  def test_updated_at_is_public_datetime(self):
    """Test that update_at attribute is the datetime object."""
    bm = BaseModel()
    self.assertEqual(datetime, type(bm.updated_at))

  def test_save_updates_at(self):
    """Test that save the method updates updated_at 
attribute."""
    bm = BaseModel()
    first_updated_at = bm.updated_at
    bm.save()
    self.assertGreater(bm.updated_at, first_updated_at)

  def test_to_dict_returns_dict(self):
    """Test to_dict method returns into dictionary."""
    bm = BaseModel()
    self.assertTrue(dict, type(bm.to_dict()))

  def test_to_dict_contains_basic_keys(self):
    """Test that to_dict include id, created_at, and updated_at."""
    bm = BaseModel()
    bm_dict = bm.to_dict()
    self.assertIn("id", bm_dict)
    self.assertIn("created_at", bm_dict)
    self.assertIn("updated_at", bm_dict)
    self.assertEqual(str, type(bm_dict["id"]))
    self.assertEqual(str, type(bm_dict["created_at"]))
    self.assertEqual(str, type(bm_dict["updated_at"]))

  if __name__ == "__main__":
    unittest.main()