#!/usr/bin/python3
""" State Module for HBNB project """
from models import my_enviroment
from models.base_model import BaseModel
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class Amenity(BaseModel, Base):
    __tablename__ = "amenities"
    
    if my_enviroment == "db":
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        super().__init__(*args, **kwargs)
