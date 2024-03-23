#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.city import City
from models.state import State


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                       .format(getenv('HBNB_MYSQL_USER'),
                                               getenv('HBNB_MYSQL_PWD'),
                                               getenv('HBNB_MYSQL_HOST'),
                                               getenv('HBNB_MYSQL_DB')),
                                       pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        from models import base_model
        objs = {}
        if cls:
            objs = {obj.id: obj for obj in self.__session.query(cls).all()}
        else:
            for cls in base_model.Base.__subclasses__():
                objs.update({obj.id: obj for obj in self.__session.query(cls).all()})
        return objs

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                      expire_on_commit=False))()
