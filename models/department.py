from models.base import BaseModel, Base
from sqlalchemy import String, Column
import models
from sqlalchemy.orm import relationship


class Department(BaseModel, Base):
    if models.storage_t == "db":
        __tablename__ = "departments"
        dept_name = Column(String(128), nullable=False)
        
        courses = relationship("Course", backref="department",
                               cascade="all, delete-orphan")
    
    else:
        dept_name = ""