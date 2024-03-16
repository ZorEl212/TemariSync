from models.base import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship
import models

class Student(BaseModel, Base):
    if models.storage_t == 'db':
        __tablename__ = 'students'
        name = Column(String(128), nullable=False)
        email = Column(String(128), nullable=True)
        school_id = Column(String(128), nullable=False)
        dept_id = Column(String(60), ForeignKey('departments.id'), nullable=False)
        documents = relationship('Document', backref='students', cascade='all, delete')
    
    else:
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
                