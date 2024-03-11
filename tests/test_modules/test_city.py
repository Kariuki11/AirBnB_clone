#!/usr/bin/python3
"""Defines unittests for models/city.py."""

import os
import unittest
from datetime import datetime
from time import sleep

from models import storage  # Assuming storage is in a module named 'models'
from models.city import City  # Replace with actual import path


class TestCity_instantiation(unittest.TestCase):
  """Unittest used for testing instantiation of the City class."""

  def test_no_args_instantiates(self):
      """Tests if City() creates an instance."""
      self.assertEqual(City, type(City()))

  def test_new_instance_stored_in_objects(self):
      """Tests if new City instance is stored in storage.all().values()."""
      city = City()  # Create an instance explicitly
      self.assertIn(city, storage.all().values())

  def test_id_is_public_str(self):
      """Tests if the City().id is of the type str."""
      self.assertEqual(str, type(City().id))

  def test_created_at_is_public_datetime(self):
      """Tests if the City().created_at is of type datetime."""
      self.assertEqual(datetime, type(City().created_at))

  def test_updated_at_is_public_datetime(self):
      """Tests if City().updated_at is of type datetime."""
      self.assertEqual(datetime, type(City().updated_at))

  def test_state_id_is_public_class_attribute(self):
      """Tests if City.state_id is a public class attribute (not instance-level)."""
      cy = City()
      self.assertEqual(str, type(City.state_id))
      self.assertIn("state_id", dir(cy))
      self.assertNotIn("state_id", cy._dict_)

  def test_name_is_public_class_attribute(self):
      """Tests if the City.name is a public class an attribute (not instance-level)."""
      cy = City()
      self.assertEqual(str, type(City.name))
      self.assertIn("name", dir(cy))
      self.assertNotIn("name", cy._dict_)

  def test_two_cities_unique_ids(self):
      """Tests if two City instances have unique IDs."""
      cy1 = City()
      cy2 = City()
      self.assertNotEqual(cy1.id, cy2.id)

  def test_two_cities_different_created_at(self):
      """Tests if two City instances have the different created_at timestamps."""
      cy1 = City()
      sleep(0.05)
      cy2 = City()
      self.assertLess(cy1.created_at, cy2.created_at)

  def test_two_cities_different_updated_at(self):
      """Tests if two City instances have different updated_at timestamps."""
      cy1 = City()
      sleep(0.05)
      cy2 = City()
      self.assertLess(cy1.updated_at, cy2.updated_at)

  def test_str_representation(self):
      """Tests the string representation of a City instance."""
      dt = datetime.today()
      dt_repr = repr(dt)
      cy = City()
      cy.id = "123456"
      cy.created_at = cy.updated_at = dt
      cystr = cy._str_()
      self.assertIn("[City] (123456)", cystr)
      self.assertIn("'id': '123456'", cystr)
      self.assertIn("'created_at': " + dt_repr, cystr)
      self.assertIn("'updated_at': " + dt_repr, cystr)

  def test_args_unused(self):
      """Tests if arguments passed to City() are not used."""
      cy = City(None)
      self.assertNotIn(None, cy._dict_.values())

  def test_instantiation_with_kwargs(self):
      """Tests instantiation with keyword arguments for id, created_at, and updated_at."""
      dt = datetime.today()
      dt_iso = dt.isoformat()
      cy = City(id="345", created_at=dt_iso, updated_at=dt_iso)
      self.assertEqual(cy.id, "345")
      self.assertEqual(cy.created_at, dt)
      self.assertEqual(cy.updated_at, dt)

  def test_instantiation_with_None_kwargs(self):
            """Tests if passing None for keyword arguments raises TypeError."""
            with self.assertRaises(TypeError):
                City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
        """Unittests for testing save method of the City class."""

        @classmethod
        def setUp(self):
            """
            Renames any existing "file.json" to "tmp" to avoid conflicts during tests.
            """
            try:
                os.rename("file.json", "tmp")
            except OSError:
                pass

        def tearDown(self):
            """
            Attempts to remove "file.json" and then rename "tmp" back to "file.json"
            if it exists, ensuring cleanup after tests.
            """
            try:
                os.remove("file.json")
            except OSError:
                pass
            try:
                os.rename("tmp", "file.json")
            except OSError:
                pass

        def test_one_save(self):
            """Tests if save() updates updated_at and stores the City instance."""
            cy = City()
            sleep(0.05)
            first_updated_at = cy.updated_at
            cy.save()
            self.assertLess(first_updated_at, cy.updated_at)
            self.assertIn(cy, storage.all().values())  # Check storage inclusion

        def test_two_saves(self):
            """Tests if multiple saves update updated_at correctly and persist changes."""
            cy = City()
            sleep(0.05)
            first_updated_at = cy.updated_at
            cy.save()
            second_updated_at = cy.updated_at
            self.assertLess(first_updated_at, second_updated_at)
            sleep(0.05)
            cy.save()
            third_updated_at = cy.updated_at
            self.assertLess(second_updated_at, third_updated_at)
            self.assertIn(cy, storage.all().values())  # Check storage inclusion

        def test_save_with_arg(self):
            """Tests if save() raises TypeError when passed an argument."""
            cy = City()
            with self.assertRaises(TypeError):
                cy.save(None)

        def test_save_updates_file(self):
            """Tests if save() writes the City instance to the storage file."""
            cy = City()
            cy.save()
            cyid = "City." + cy.id
            with open("file.json", "r") as f:
                self.assertIn(cyid, f.read())


class TestCity_to_dict(unittest.TestCase):
        """Unittests for testing to_dict method of the City class."""

        def test_to_dict_type(self):
            """Tests if City().to_dict() returns a dictionary."""
            self.assertTrue(dict, type(City().to_dict()))

        def test_to_dict_contains_correct_keys(self):
            """Tests if to_dict() includes essential keys (id, created_at, updated_at, _class_)"""
            cy = City()
            self.assertIn("id", cy.to_dict())
            self.assertIn("created_at", cy.to_dict())
            self.assertIn("updated_at", cy.to_dict())
            self.assertIn("_class_", cy.to_dict())

        def test_to_dict_contains_added_attributes(self):
            """Tests if to_dict() includes additional instance attributes."""
            cy = City()
            cy.middle_name = "Holberton"
            cy.my_number = 98
            self.assertEqual("Holberton", cy.middle_name)
            self.assertIn("my_number", cy.to_dict())

        def test_to_dict_datetime_attributes_are_strs(self):
            """Tests if to_dict() converts datetime attributes to strings."""
            cy = City()
            cy_dict = cy.to_dict()
            self.assertEqual(str, type(cy_dict["id"]))
            self.assertEqual(str, type(cy_dict["updated_at"]))
            self.assertEqual(str, type(cy_dict["created_at"]))
            self.assertEqual(str, type(cy_dict["updated_at"]))

        
        def test_to_dict_output(self):
                                     
                dt = datetime.today()
                cy = City()
                cy.id = "123456"
                cy.created_at = cy.updated_at = dt
                tdict = {
                    'id': '123456',
                    '_class_': 'City',
                    'created_at': dt.isoformat(),
                    'updated_at': dt.isoformat(),
                }
                self.assertDictEqual(cy.to_dict(), tdict)

        def test_contrast_to_dict_dunder_dict(self):
                """Tests if to_dict() is different from the private _dict_ attribute."""
                cy = City()
                self.assertNotEqual(cy.to_dict(), cy._dict_)

        def test_to_dict_with_arg(self):
                """Tests if to_dict() raises TypeError when passed an argument."""
                cy = City()
                with self.assertRaises(TypeError):
                    cy.to_dict(None)


if __name__ == "__main__":
    unittest.main()
