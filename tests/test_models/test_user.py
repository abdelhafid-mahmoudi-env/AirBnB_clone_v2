#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.user import User
from models.base_model import BaseModel
from models import my_enviroment
import unittest

class TestUser(unittest.TestCase):
    """Test cases for the User class."""
    def test_is_subclass(self):
        """Test if User is a subclass of BaseModel."""
        user = User()
        self.assertIsInstance(user, BaseModel)
        self.assertTrue(hasattr(user, "id"))
        self.assertTrue(hasattr(user, "created_at"))
        self.assertTrue(hasattr(user, "updated_at"))

    def test_email_attr(self):
        """Test that User has attribute 'email', and it's an empty string."""
        user = User()
        self.assertTrue(hasattr(user, "email"))
        if my_enviroment == 'db':
            self.assertEqual(user.email, None)
        else:
            self.assertEqual(user.email, "")

    def test_password_attr(self):
        """Test that User has attribute 'password', and it's an empty string."""
        user = User()
        self.assertTrue(hasattr(user, "password"))
        if my_enviroment == 'db':
            self.assertEqual(user.password, None)
        else:
            self.assertEqual(user.password, "")

    def test_first_name_attr(self):
        """Test that User has attribute 'first_name', and it's an empty string."""
        user = User()
        self.assertTrue(hasattr(user, "first_name"))
        if my_enviroment == 'db':
            self.assertEqual(user.first_name, None)
        else:
            self.assertEqual(user.first_name, "")

    def test_last_name_attr(self):
        """Test that User has attribute 'last_name', and it's an empty string."""
        user = User()
        self.assertTrue(hasattr(user, "last_name"))
        if my_enviroment == 'db':
            self.assertEqual(user.last_name, None)
        else:
            self.assertEqual(user.last_name, "")

    def test_to_dict_creates_dict(self):
        """Test if the to_dict method creates a dictionary with proper attributes."""
        u = User()
        new_d = u.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in u.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """Test that values in the dictionary returned from to_dict are correct."""
        time = "%Y-%m-%dT%H:%M:%S.%f"
        u = User()
        new_d = u.to_dict()
        self.assertEqual(new_d["__class__"], "User")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], u.created_at.strftime(time))
        self.assertEqual(new_d["updated_at"], u.updated_at.strftime(time))

    def test_str(self):
        """Test that the str method has the correct output."""
        user = User()
        string = "[User] ({}) {}".format(user.id, user.__dict__)
        self.assertEqual(string, str(user))

