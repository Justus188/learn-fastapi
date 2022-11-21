from pydantic import BaseModel, EmailStr
from typing import List

# Models for JSON input/output data validation. See models.py for SQLAlchemy models for DB.

class OrmModel(BaseModel):
    class Config():
        orm_mode = True

class User(OrmModel):
    username: str
    email: EmailStr

class Blog(OrmModel):
    title: str
    body: str

class UserOut(User):
    blogs: List[Blog] = []
    
class UserCreate(User):
    password: str

class UserWrite(User):
    hashed_password: str

class BlogOut(Blog):
    id: int
    user: User