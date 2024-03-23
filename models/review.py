#!/usr/bin/python3
""" Review module for the HBNB project """
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base
from models import my_enviroment


class Review(BaseModel, Base):

    __tablename__ = 'reviews'
    if my_enviroment == "db":
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)
