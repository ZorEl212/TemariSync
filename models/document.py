#!/usr/bin/env python3
"""Module for documents view
"""

from models.base import BaseModel, Base
import models
from datetime import datetime
import shutil
from sqlalchemy import Column, String, ForeignKey, Text, Table
import os
from sqlalchemy.orm import relationship


class Document(BaseModel, Base):
    """Document class for the documents
    Attributes:
        title: title of the document
        category: category of the document
        file_type: type of the file (pdf, docx, etc)
        course_id: id of the course
        stud_id: id of the student who uploaded the document
        tags: tags associated with the document
        filename: name of the file in the server
        description: description of the document
        author_comment: comment by the author"""

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
        """Updates time metadata of an instance and saves it on main dictionary
        args:
            file: file to be saved
            tags: tags to be associated with the document"""

        if file is not None:
            base, extension = os.path.splitext(os.path.basename(file))
            self.filename = f'{self.id}{extension}'
            doc_dir = os.getenv("DOC_DIR")
            os.makedirs(doc_dir, exist_ok=True)
            dest_file = os.path.join(doc_dir, self.filename)
            shutil.copy(file, dest_file)
            self.file_type = extension.split('.')[1].upper()

        # Tag Handling
        if tags is not None:
            # Clear existing tags if any and append new tags
            self.tags.clear()
            for tag_name in tags:
                tag = Tag.get_or_create(name=tag_name)
                self.tags.append(tag)

        setattr(self, 'updated_at', datetime.now())
        models.storage.save()


    def get_file(self):
        """Returns the relative path of the document file in the server"""

        extension = os.path.splitext(self.filename)[-1]

        # Ensure directories exist
        return_dir = os.getenv("RETURN_DIR")
        doc_dir = os.getenv("DOC_DIR")
        os.makedirs(return_dir, exist_ok=True)
        dest_dir = os.path.join(return_dir, str(self.id))
        os.makedirs(dest_dir, exist_ok=True)

        # Construct destination file path
        dest_file = os.path.join(dest_dir, f"{self.title}{extension}")

        shutil.copy2(os.path.join(doc_dir, self.filename), dest_file)

        return os.path.relpath(dest_file, start=return_dir)


class Tag(BaseModel, Base):
    """Tag class for the documents
    Attributes:
        name: name of the tag"""

    __tablename__ = "tags"
    id = Column(String(60), primary_key=True)
    name = Column(String(128), nullable=False)

    @classmethod
    def get_or_create(cls, name):
        """Returns a tag with the given name if it exists, else creates a new tag
        args:
            name: name of the tag"""

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
