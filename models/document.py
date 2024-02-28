from models.base import BaseModel
import models
from datetime import datetime
import shutil
import os
class Document(BaseModel):
    title = ""
    category = ""
    course_id = ""
    stud_id = ""
    tags = []
    filename= ""

    def save(self, file=None):
        """Updates time metadata of an instance and saves it on main dictionary"""
        
        if file is not None:
            base, extention = os.path.splitext(os.path.basename(file))
            self.filename = f'{self.id}{extention}'
            shutil.copy(file, f'{os.getenv("DOC_DIR")}{self.filename}')
        setattr(self, 'updated_at', datetime.now())
        models.storage.save()

    def get_file(self):
        extention = os.path.splitext(self.filename)[-1]
        if not os.path.exists(f'{os.getenv("RETURN_DIR")}{self.id}'):
            os.mkdir(path=f'{os.getenv("RETURN_DIR")}{self.id}')
        shutil.copy2(f'{os.getenv("DOC_DIR")}{self.filename}',
                     f'{os.getenv("RETURN_DIR")}{self.id}/{self.title}{extention}')
        return f'{self.id}/{self.title}{extention}'
