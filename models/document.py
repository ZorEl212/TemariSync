from models.base import BaseModel, Base
import models
from datetime import datetime
import shutil
from sqlalchemy import Column, String, ForeignKey, Text, Table
import os
from sqlalchemy.orm import relationship

class Document(BaseModel, Base):
    __tablename__ = "documents"
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        title = Column(String(128), nullable=False)
        category = Column(String(128), nullable=False)
        file_type = Column(String(128), nullable=False)
        course_id = Column(String(60), ForeignKey('courses.id'), nullable=False)
        stud_id = Column(String(60), ForeignKey('students.id'), nullable=False)
        filename = Column(String(128), nullable=False)
        description = Column(Text, nullable=False)
        author_comment = Column(Text, nullable=False)
        tags = relationship('Tag', secondary='document_tags', backref='documents')

    else:
        title = ""
        category = ""
        file_type = ""
        course_id = ""
        stud_id = ""
        tags = []
        filename= ""
        description = ""
        author_comment =""

    def save(self, file=None, tags=None):
        """Updates time metadata of an instance and saves it on main dictionary"""
        
        if file is not None:
            base, extension = os.path.splitext(os.path.basename(file))
            self.filename = f'{self.id}{extension}'
            os.makedirs(os.getenv("DOC_DIR"), exist_ok=True)
            shutil.copy(file, f'{os.getenv("DOC_DIR")}{self.filename}')
            self.file_type = extension.split('.')[1].upper()
        if tags is not None:
            self.tags.clear()
            for tag_name in tags:
                tag = Tag.get_or_create(name=tag_name)
                if tag not in self.tags:
                    self.tags.append(tag)
        setattr(self, 'updated_at', datetime.now())
        models.storage.save()

    def get_file(self):
        extention = os.path.splitext(self.filename)[-1]
        os.makedirs(os.getenv("RETURN_DIR"), exist_ok=True)
        if not os.path.exists(f'{os.getenv("RETURN_DIR")}{self.id}'):
            os.mkdir(path=f'{os.getenv("RETURN_DIR")}{self.id}')
        shutil.copy2(f'{os.getenv("DOC_DIR")}{self.filename}',
                     f'{os.getenv("RETURN_DIR")}{self.id}/{self.title}{extention}')
        return f'{self.id}/{self.title}{extention}'

class Tag(BaseModel, Base):
    __tablename__ = "tags"
    id = Column(String(60), primary_key=True)
    name = Column(String(128), nullable=False)

    @classmethod
    def get_or_create(cls, name):
        tags = models.storage.all(cls)
        t = None
        for tag in tags.values():
            if tag.name == name:
                t = tag

        if t is None:
            tag = cls(name=name)
            tag.save()
            t = tag
        return t

document_tags = Table('document_tags', Base.metadata,
    Column('document_id', String(60), ForeignKey('documents.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('tag_id', String(60), ForeignKey('tags.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
)
