from models.base import BaseModel
import models

class Student(BaseModel):
    name = ""
    email = ""
    school_id = ""
    dept_id = ""

    @property
    def documents(self):
        all = models.storage.all()
        docs = {}
        for key, values in all.items():
            if hasattr(values, 'stud_id'):
                if values.cls_name == 'Document' and values.stud_id == self.id:
                    docs[key] = values
        return docs

    @property
    def department(self):
        all = models.storage.all()
        for key, values in all.items():
            if values.cls_name == 'Department' and values.id == self.dept_id:
                return values.name
                