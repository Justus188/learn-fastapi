from sqlalchemy import Column, Integer, String, ForeignKey #Float, Boolean
from sqlalchemy.orm import relationship

from database import Base

# Models for SQLAlchemy DB. See schemas.py for JSON Input / Output data validation.

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key = True, index = True)
    username= Column(String)
    email = Column(String)
    hashed_password = Column(String)

    blogs = relationship("Blog", back_populates='user')

class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates = "blogs")