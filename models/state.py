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
            """
            Returns the list of City objects from storage linked to the current State
            """
            from models import storage
            from models.city import City

            all_cities = storage.all(City)
            state_cities = [
                    city for city in all_cities.values()
                    if city.state_id == self.id
            ]
            return state_cities

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)
