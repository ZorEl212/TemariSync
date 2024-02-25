from models.base import BaseModel
import models

class Course(BaseModel):
    """Course Class"""

    name = ""
    dept_id = ""

    @property
    def documents(self):
        all = models.storage.all()
        docs = {}
        for key, values in all.items():
            if hasattr(values, 'course_id'):
                if values.cls_name == 'Document' and values.course_id == self.id:
                    docs[key] = values
        return docs
