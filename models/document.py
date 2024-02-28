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

    def save(self, file):
        """Updates time metadata of an instance and saves it on main dictionary"""

        setattr(self, 'updated_at', datetime.now())
        base, extention = os.path.splitext(os.path.basename(file))
        self.filename = f'{self.id}{extention}'
        shutil.copy(file, f'docs/{self.filename}')
        models.storage.save()

    def get_file(self):
        extention = os.path.splitext(self.filename)[-1]
        if not os.path.exists(f'return/{self.id}'):
            os.mkdir(path=f'return/{self.id}')
        shutil.copy2(f'docs/{self.filename}', f'return/{self.id}/{self.title}{extention}')
        return f'{self.id}/{self.title}{extention}'
