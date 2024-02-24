from uuid import uuid4
from datetime import datetime
import models
class BaseModel:
    def __init__(self, **kwargs):
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
        return f"[{self.cls_name}] ({self.id}) {self.__dict__}"

    def save(self):
        setattr(self, 'updated_at', datetime.now())
        models.storage.save()

    @classmethod
    def get_cls_name(cls):
        return cls.__name__

    @property
    def cls_name(self):
        return self.get_cls_name()

    def to_dict(self):
        res = vars(self)
        for key, value in res.items():
            if key in ['created_at', 'updated_at']:
                res[key] = value.isoformat(timespec='microseconds')
        res['__class__'] = self.cls_name
        return res
            
        