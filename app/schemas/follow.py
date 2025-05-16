from pydantic import BaseModel

class FollowCreate(BaseModel):
    following_id: int

class FollowRead(BaseModel):
    id: int
    follower_id: int
    following_id: int

    class Config:
        orm_mode = True