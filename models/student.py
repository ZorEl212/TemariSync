#!/usr/bin/python3
"""Module for students view"""

from flask_login import UserMixin
from models.base import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey, Text
from sqlalchemy.orm import relationship
import models
from werkzeug.security import generate_password_hash, check_password_hash

class Student(BaseModel, UserMixin, Base):
    """Student class for the students
    Attributes:
        name: name of the student
        email: email of the student
        school_id: school id of the student
        _password: password of the student
        dept_id: id of the department
        documents: documents uploaded by the student
        department: department of the student"""

    if models.storage_t == 'db':
        __tablename__ = 'students'
        name = Column(String(128), nullable=False)
        email = Column(String(128), nullable=True)
        school_id = Column(String(128), nullable=False)
        _password = Column('password', Text, nullable=False)
        dept_id = Column(String(60), ForeignKey('departments.id'), nullable=False)
        documents = relationship('Document', backref='students', cascade='all, delete')
    
    else:
        name = ""
        email = ""
        school_id = ""
        dept_id = ""

        @property
        def documents(self):
            """Returns all the documents uploaded by the student"""
            all = models.storage.all()
            docs = {}
            for key, values in all.items():
                if hasattr(values, 'stud_id'):
                    if values.cls_name == 'Document' and values.stud_id == self.id:
                        docs[key] = values
            return docs
    
        @property
        def department(self):
            """Returns the department of the student"""
            all = models.storage.all()
            for key, values in all.items():
                if values.cls_name == 'Department' and values.id == self.dept_id:
                    return values.name

    @property
    def password(self):
        return AttributeError('Password is not a readable attribute')

    def set_password(self, password):
        self._password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self._password, password)