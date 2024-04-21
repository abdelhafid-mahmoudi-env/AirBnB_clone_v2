#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models import my_enviroment


class State(BaseModel, Base):
    """Representation of state """
    __tablename__ = 'states'
    if my_enviroment == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    else:
        @property
        def cities(self):
            """ Gets a list of all cities in state """
            return [city for city in models.storage.all(City).values() if
                    self.id == city.state_id]

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)
