#!/usr/bin/python3
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Relationship, sessionmaker, scoped_session

from models.base import BaseModel, Base
from models.course import Course
from models.department import Department
from models.document import Document
from models.student import Student

classes = [Course, Department, Document, Student]

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Initialization method."""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@localhost/{}'
                                      .format(getenv('TS_DB_USER'),
                                              getenv('TS_DB_PWD'),
                                              getenv('TS_DB')),
                                      pool_pre_ping=True)
        if getenv('TS_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return a dictionary of all instances of a class."""
        res = {}
        if isinstance(cls, str) and eval(cls) in classes:
            for instance in self.__session.query(eval(cls)).all():
                key = "{}.{}".format(cls, instance.id)
                res[key] = instance
        elif cls is None:
            for cls in classes:
                for inst in self.__session.query(cls).all():
                    key = "{}.{}".format(inst.cls_name, inst.id)
                    res[key] = inst
        else:
            for instance in self.__session.query(cls).all():
                    res[instance.id] = instance
        return res

    def new(self, obj):
        """Add a new instance to the session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the database."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an instance from the session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the session."""
        self.__session.close()
        
    def get(self, cls, id):
        if (eval(cls) if isinstance(cls, str) else cls) in classes:
            all = self.all(cls)
            for value in all.values():
                if value.id == id:
                    return value
        return None

    def count(self, cls=None):
        if cls is not None:
            all_cls = self.all(cls)
            return len(all_cls)
        else:
            count = 0
            for cls in classes:
                count += self.count(cls)
            return count
