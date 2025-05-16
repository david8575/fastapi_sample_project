from pydantic import BaseModel
from typing import Optional

class PostCreate(BaseModel):
    content: Optional[str] = None
    image_url: Optional[str] = None

class PostRead(BaseModel):
    id: int
    user_id: int
    content: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        orm_mode = True