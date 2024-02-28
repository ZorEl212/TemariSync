from json import dump, load
import os
from copy import deepcopy
from models.base import BaseModel
from models.course import Course
from models.department import Department
from models.student import Student
from models.document import Document

class FileStorage:
    """Class for implementing JSON based file storage"""

    __objs = {}
    classes = ['Student', 'Department', 'Course', 'Document']
    __path = 'file.json'

    def all(self, cls=None):
        """Fetch all objects that exist on the file storage"""
        if cls is not None:
            o = {}
            for key, value in self.__objs.items():
                if value.cls_name == cls if isinstance(cls, str) else isinstance(value, cls):
                    o[key] = value
            return o
        return self.__objs

    def new(self, obj):
        """Add new object to the main dict before saving to File"""
        self.__objs[f"{obj.cls_name}.{obj.id}"] = obj

    def save(self):
        """Save all objects from native dict to a JSON file"""
        objs = deepcopy(self.__objs)
        with open(self.__path, 'w+') as file:
            data = {key: value.to_dict() for key, value in
                    objs.items()}
            dump(data, file)

    def reload(self):
        """Reload objects from JSON file to main dict object"""
        if os.path.exists(self.__path):
            with open(self.__path, 'r') as file:
                data = load(file)
            for ser_data in data.values():
                cls_name = ser_data.get('__class__')
                if cls_name in self.classes:
                    new_obj = eval(cls_name)(**ser_data)
                    self.new(new_obj)

    def count(self, cls=None):
        """Get count of objects based on class"""
        count = 0
        if cls is None:
            return len(self.__objs)
        elif cls in self.classes or cls.__name__ in self.classes:
            for obj in __class__.__objs.values():
                if obj.cls_name == cls if isinstance(
                    cls, str) else isinstance(obj, cls):
                    #To explain what's going on here,
                    #if cls is a string it will be compared
                    #with the class name otherwise if cls is
                    #a class type, obj will be checked
                    #if it's an instance of cls
                    count += 1     
        return count

    def get(self, cls, id):
        """Get a object based on given id"""
        obj = {}
        if isinstance(cls, str):
            if cls not in self.classes:
                return None
            for o in self.__objs.values():
                if isinstance(o, eval(cls)) and o.to_dict()['id'] == id:
                    return o
        elif cls.__name__ in self.classes:
            print("Yes")
            for o in self.__objs.values():
                if isinstance(o, cls) and o.to_dict()['id'] == id:
                    return o
        return None    
    def delete(self, obj):
        __class__.__objs.pop(f"{obj.cls_name}.{obj.id}")
        self.save()
        self.reload()         

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
