#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.city import City
from models.base_model import BaseModel
from models import my_enviroment
import unittest

class test_City(unittest.TestCase):
    """ """

    def test_is_subclass(self):
        """Test that City is a subclass of BaseModel."""
        city = City()
        self.assertIsInstance(city, BaseModel)
        self.assertTrue(hasattr(city, "id"))
        self.assertTrue(hasattr(city, "created_at"))
        self.assertTrue(hasattr(city, "updated_at"))

    def test_name_attr(self):
        """Test that City has attribute 'name', and it's an empty string."""
        city = City()
        self.assertTrue(hasattr(city, "name"))
        if my_enviroment == 'db':
            self.assertEqual(city.name, None)
        else:
            self.assertEqual(city.name, "")

    def test_state_id_attr(self):
        """Test that City has attribute 'state_id', and it's an empty string."""
        city = City()
        self.assertTrue(hasattr(city, "state_id"))
        if my_enviroment == 'db':
            self.assertEqual(city.state_id, None)
        else:
            self.assertEqual(city.state_id, "")

    def test_to_dict_creates_dict(self):
        """Test if the to_dict method creates a dictionary with proper attributes."""
        c = City()
        new_d = c.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in c.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """Test that values in the dictionary returned from to_dict are correct."""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        c = City()
        new_d = c.to_dict()
        self.assertEqual(new_d["__class__"], "City")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], c.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], c.updated_at.strftime(t_format))

    def test_str(self):
        """Test that the str method has the correct output."""
        city = City()
        string = "[City] ({}) {}".format(city.id, city.__dict__)
        self.assertEqual(string, str(city))
