from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """Base class containing all common attributes and methods 
    for other classes"""

    def __init__(self, **kwargs):
        """Init point
            Args:
                kwargs: arbirary dict of args"""

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
        """Return dict structure of an instance."""

        return f"[{self.cls_name}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates time metadata of an instance and saves it on main dictionary"""

        setattr(self, 'updated_at', datetime.now())
        models.storage.save()

    @classmethod
    def get_cls_name(cls):
        return cls.__name__

    @property
    def cls_name(self):
        """return a string value which is the class name an 
        instance is created from"""

        return self.get_cls_name()

    def to_dict(self):
        """Returns dictionary representation of an instance more suited for
            serialzing to JSON file"""

        res = vars(self)
        for key, value in res.items():
            if key in ['created_at', 'updated_at']:
                res[key] = value.isoformat(timespec='microseconds')
        res['__class__'] = self.cls_name
        return res
            
        