from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    birthdate: Optional[date] = None
    address: Optional[str] = None

class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None

    class Config:
        orm_mode = True
