from json import dump, load
import os
from copy import deepcopy
from models.base import BaseModel
from models.course import Course
from models.department import Department
from models.student import Student
from models.document import Document

class FileStorge:

    __objs = {}
    classes = ['Student', 'Department', 'Course', 'Document', 'BaseModel']
    __path = 'file.json'

    def all(self):
        return self.__objs

    def new(self, obj):
        self.__objs[f"{obj.cls_name}.{obj.id}"] = obj

    def save(self):
        objs = deepcopy(self.__objs)
        with open(self.__path, 'w+') as file:
            data = {key: value.to_dict() for key, value in
                    objs.items()}
            dump(data, file)

    def reload(self):
        if os.path.exists(self.__path):
            with open(self.__path, 'r') as file:
                data = load(file)
            for ser_data in data.values():
                cls_name = ser_data.get('__class__')
                if cls_name in self.classes:
                    new_obj = eval(cls_name)(**ser_data)
                    self.new(new_obj)
