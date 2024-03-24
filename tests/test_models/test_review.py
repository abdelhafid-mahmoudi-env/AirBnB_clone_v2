#!/usr/bin/python3
""" """
from models.review import Review
from models.base_model import BaseModel
from models import my_enviroment
import unittest

class test_review(unittest.TestCase):
    """ """

    def test_is_subclass(self):
        """Test if Review is a subclass of BaseModel."""
        review = Review()
        self.assertIsInstance(review, BaseModel)
        self.assertTrue(hasattr(review, "id"))
        self.assertTrue(hasattr(review, "created_at"))
        self.assertTrue(hasattr(review, "updated_at"))

    def test_place_id_attr(self):
        """Test Review has attribute 'place_id', and it's an empty string."""
        review = Review()
        self.assertTrue(hasattr(review, "place_id"))
        if my_enviroment == 'db':
            self.assertEqual(review.place_id, None)
        else:
            self.assertEqual(review.place_id, "")

    def test_user_id_attr(self):
        """Test Review has attribute 'user_id', and it's an empty string."""
        review = Review()
        self.assertTrue(hasattr(review, "user_id"))
        if my_enviroment == 'db':
            self.assertEqual(review.user_id, None)
        else:
            self.assertEqual(review.user_id, "")

    def test_text_attr(self):
        """Test Review has attribute 'text', and it's an empty string."""
        review = Review()
        self.assertTrue(hasattr(review, "text"))
        if my_enviroment == 'db':
            self.assertEqual(review.text, None)
        else:
            self.assertEqual(review.text, "")

    def test_to_dict_creates_dict(self):
        """Test if the to_dict method creates a dictionary with proper attributes."""
        r = Review()
        new_d = r.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in r.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """Test that values in the dictionary returned from to_dict are correct."""
        time = "%Y-%m-%dT%H:%M:%S.%f"
        r = Review()
        new_d = r.to_dict()
        self.assertEqual(new_d["__class__"], "Review")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], r.created_at.strftime(time))
        self.assertEqual(new_d["updated_at"], r.updated_at.strftime(time))

    def test_str(self):
        """Test that the str method has the correct output."""
        review = Review()
        string = "[Review] ({}) {}".format(review.id, review.__dict__)
        self.assertEqual(string, str(review))
