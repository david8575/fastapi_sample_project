from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    psot_id: int 
    content: str

class CommentRead(BaseModel):
    id: int
    user_id: int
    post_id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True