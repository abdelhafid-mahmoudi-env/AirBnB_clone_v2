#!/usr/bin/python3
""" """
from models.state import State
from models.base_model import BaseModel
from models import my_enviroment
import unittest

class TestState(unittest.TestCase):
    """Test cases for the State class."""
    def test_is_subclass(self):
        """Test if State is a subclass of BaseModel."""
        state = State()
        self.assertIsInstance(state, BaseModel)
        self.assertTrue(hasattr(state, "id"))
        self.assertTrue(hasattr(state, "created_at"))
        self.assertTrue(hasattr(state, "updated_at"))

    def test_name_attr(self):
        """Test that State has attribute 'name', and it's an empty string."""
        state = State()
        self.assertTrue(hasattr(state, "name"))
        if my_enviroment == 'db':
            self.assertEqual(state.name, None)
        else:
            self.assertEqual(state.name, "")

    def test_to_dict_creates_dict(self):
        """Test if the to_dict method creates a dictionary with proper attributes."""
        s = State()
        new_d = s.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in s.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """Test that values in the dictionary returned from to_dict are correct."""
        time = "%Y-%m-%dT%H:%M:%S.%f"
        s = State()
        new_d = s.to_dict()
        self.assertEqual(new_d["__class__"], "State")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], s.created_at.strftime(time))
        self.assertEqual(new_d["updated_at"], s.updated_at.strftime(time))

    def test_str(self):
        """Test that the str method has the correct output."""
        state = State()
        string = "[State] ({}) {}".format(state.id, state.__dict__)
        self.assertEqual(string, str(state))
