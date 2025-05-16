from sqlalchemy import Column, Integer, Text, VARCHAR, TIMESTAMP, ForeignKey 
from app.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_id", ondelete="CASCADE"), nullable=False)
    content = Column(Text)
    image_url = Column(VARCHAR(255))
    created_at = Column(TIMESTAMP)