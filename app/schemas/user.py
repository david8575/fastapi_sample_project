from pydantic import BaseModel, EmailStr

# 입력용 스키마
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    # 이후 항목 추가하면 됨

# 응답용 스키마
class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr

# 로그인용 스키마
class UserLogin(BaseModel):
    email: EmailStr
    password: str