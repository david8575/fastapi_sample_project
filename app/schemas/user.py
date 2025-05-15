from pydantic import BaseModel, EmailStr
from typing import Optional, List

# 입력용 스키마
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# 응답용 스키마
class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    followers: List[int] = []
    following: List[int] = []

# 로그인용 스키마
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 사용자 정보용 스키마
class UserUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    followers: List
    following: List