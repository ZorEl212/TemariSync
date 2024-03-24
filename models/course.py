#!/usr/bin/python3
"""Module for courses view"""

from models.base import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship
import models


class Course(BaseModel, Base):
    """Course Class
    attributes:
        name: name of the course
        dept_id: id of the department
        documents: documents belonging to the course"""

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
            """Returns all the documents blonging to the course"""
            all = models.storage.all()
            docs = {}
            for key, values in all.items():
                if hasattr(values, 'course_id'):
                    if values.cls_name == 'Document' and values.course_id == self.id:
                        docs[key] = values
            return docs
    