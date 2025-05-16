from sqlalchemy import Column, Integer, String, Text, Date, TIMESTAMP
from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    bio = Column(Text)
    profile_image_url = Column(String(255))
    birthdate = Column(Date)
    address = Column(Text)
    post_count = Column(Integer)
    followers_count = Column(Integer)
    following_count = Column(Integer)
    created_at = Column(TIMESTAMP)
