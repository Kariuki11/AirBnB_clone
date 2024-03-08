#!/usr/bin/python3

"""Defines unittests for models/review.py.

*Note:* This assumes the existence of a Review class defined in models/review.py
"""

import os
import unittest
import models
import random
import string
from datetime import datetime
from time import sleep
from models import storage  
from models.review import Review
from unittest.mock import patch

class TestReview_instantiation(unittest.TestCase):
  """Unittests for testing instantiation of Review class."""

  # ... (existing test cases)

  def test_invalid_id_type(self):
      """Test for creating a Review with a non-string ID raises a TypeError."""
      with self.assertRaises(TypeError):
          Review(id=123)  # Example with the integer ID

  def test_random_string_id(self):
      """Test for creating a Review with random string ID works correctly."""
      id_length = 10  # Example of length for random ID
      random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=id_length))
      rv = Review(id=random_id)
      self.assertEqual(random_id, rv.id)

  def test_kwargs_with_extra_keys(self):
      """Test for creating Review with extra kwargs doesn't cause errors."""
      dt = datetime.today()
      dt_iso = dt.isoformat()
      rv = Review(id="345", created_at=dt_iso, updated_at=dt_iso, extra_attr="value")
      self.assertEqual(rv.id, "345")
      self.assertEqual(rv.created_at, dt)
      self.assertEqual(rv.updated_at, dt)
      self.assertNotIn("extra_attr", rv._dict_)

  class TestReview_save(unittest.TestCase):
    """Unittests for testing the save method of the Review class."""

    @classmethod
    def setUpClass(cls):
      """Prepares a clean file for testing."""
      try:
        os.remove("file.json")
      except FileNotFoundError:
        pass

    def test_one_save(self):
      """Tests that saves updates in updated_at attribute and persists to storage."""
      rv = Review()
      sleep(0.05)  # Introduces a slight delay
      first_updated_at = rv.updated_at
      rv.save()
      self.assertLess(first_updated_at, rv.updated_at)
      self.assertIn(rv.id, models.storage.all().keys())  # Checks if saved in storage

    def test_two_saves(self):
      """Tests that multiple saves update in the updated_at and persist correctly."""
      rv = Review()
      sleep(0.05)
      first_updated_at = rv.updated_at
      rv.save()
      second_updated_at = rv.updated_at
      self.assertLess(first_updated_at, second_updated_at)
      sleep(0.05)
      rv.save()
      self.assertLess(second_updated_at, rv.updated_at)
      self.assertIn(rv.id, models.storage.all().keys())  # Check existence in storage

    def test_save_with_arg(self):
      """Tests that save raises a TypeError when given an argument."""
      rv = Review()
      with self.assertRaises(TypeError):
        rv.save(None)

    @patch('models.storage.save_object')  # Mock the save_object function
    def test_save_calls_storage_save(self, mock_save):
      """Tests that saves the calls storage.save_object method."""
      rv = Review()
      rv.save()
      mock_save.assert_called_once_with(rv)  # Verifys the mock was called with the review

    def tearDownClass(cls):
      """Removes temporary file after all tests."""
      try:
        os.remove("file.json")
      except FileNotFoundError:
        pass

class TestReview_save(unittest.TestCase):
  """Unittests for testing the save method of the Review class."""

  @classmethod
  def setUpClass(cls):
    """Prepares a clean file for testing."""
    try:
      os.remove("file.json")
    except FileNotFoundError:
      pass

  def test_one_save(self):
    """Tests that saves updates in updated_at attribute and persists to storage."""
    rv = Review()
    sleep(0.05)  # Introduces a slight delay
    first_updated_at = rv.updated_at
    rv.save()
    self.assertLess(first_updated_at, rv.updated_at)
    self.assertIn(rv.id, models.storage.all().keys())  # Check if saved in the storage

  def test_two_saves(self):
    """Tests that multiple saves update updated_at and persist correctly."""
    rv = Review()
    sleep(0.05)
    first_updated_at = rv.updated_at
    rv.save()
    second_updated_at = rv.updated_at
    self.assertLess(first_updated_at, second_updated_at)
    sleep(0.05)
    rv.save()
    self.assertLess(second_updated_at, rv.updated_at)
    self.assertIn(rv.id, models.storage.all().keys())  # Checks existence in storage

  def test_save_with_arg(self):
    """Tests that saves and raises a TypeError when given an argument."""
    rv = Review()
    with self.assertRaises(TypeError):
      rv.save(None)

  @patch('models.storage.save_object')  # Mock the save_object function
  def test_save_calls_storage_save(self, mock_save):
    """Test that saves calls the storage.save_object methods."""
    rv = Review()
    rv.save()
    mock_save.assert_called_once_with(rv)  # Verify the mock was called with the review

  def tearDownClass(cls):
    """Removes temporary file after all tests."""
    try:
      os.remove("file.json")
    except FileNotFoundError:
      pass

# if _name_ == "_main_":
#   unittest.main()