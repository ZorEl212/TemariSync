from models.base import BaseModel

class Document(BaseModel):
    title = ""
    category = ""
    course_id = ""
    stud_id = ""
    tags = []