from models.base import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship
import models

class Course(BaseModel, Base):
    """Course Class"""

    if models.storage_t == 'db':
        __tablename__ = 'courses'
        name = Column(String(128), nullable=False)
        dept_id = Column(String(60), ForeignKey('departments.id'), nullable=False)
        documents = relationship('Document', backref='course', cascade='all, delete-orphan')

    else:
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
    