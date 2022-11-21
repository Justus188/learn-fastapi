from sqlalchemy import Column, Integer, String, ForeignKey, DateTime #Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base

# Models for SQLAlchemy DB. See schemas.py for JSON Input / Output data validation.

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key = True, index = True)
    username= Column(String(255), unique = True)
    email = Column(String(255), unique = True)
    hashed_password = Column(String(255))

    # role = Column(String(10))

    created_at = Column(DateTime, nullable = False, server_default = func.now())

    blogs = relationship("Blog", back_populates='user')

class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String(255))
    body = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates = "blogs")