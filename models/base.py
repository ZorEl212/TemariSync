from uuid import uuid4
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from sqlalchemy import String, Column, DateTime

Base = declarative_base()
if not getenv('STORAGE_TYPE') == 'db':
    Base = object

class BaseModel:
    """Base class containing all common attributes and methods 
    for other classes"""
    if getenv('STORAGE_TYPE') == 'db':
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, **kwargs):
        """Initialization method.
        
        Args:
            kwargs (dict): Arbitrary keyword arguments.
        """
    
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        for key, value in kwargs.items():
            if key in ['created_at', 'updated_at'] and isinstance(value, str):
                value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
            if key != '__class__':
                setattr(self, key, value)
        models.storage.new(self)

    def __str__(self):
        """Return string representation of an instance."""
        return f"[{self.cls_name}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates time metadata of an instance and saves it on main dictionary."""
        self.updated_at = datetime.now()
        models.storage.save()

    @classmethod
    def get_cls_name(cls):
        """Return the class name."""
        return cls.__name__

    @property
    def cls_name(self):
        """Return the class name an instance is created from."""
        return self.get_cls_name()

    def to_dict(self):
        """Returns dictionary representation of an instance more suited for
        serializing to JSON file."""
        res = vars(self)
        for key, value in res.items():
            if key in ['created_at', 'updated_at']:
                if isinstance(value, datetime):
                    res[key] = value.isoformat(timespec='microseconds')
                else:
                    datetime_obj = datetime.strptime(value,  '%Y-%m-%dT%H:%M:%S.%f')
                    res[key] = datetime_obj.isoformat(timespec='microseconds')
        res['__class__'] = self.cls_name
        if '_sa_instance_state' in res:
            del res['_sa_instance_state']
        if 'tags' in res:
            res['tags'] = [tag.name for tag in res['tags']]
        return res
