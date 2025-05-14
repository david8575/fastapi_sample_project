from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from app.schemas.user import UserCreate, UserRead, UserLogin
from app.schemas.token import Token
from app.services.security import hash_password, verify_password
from app.services.jwt import create_access_token, verify_access_token


# 더미 데이터
fake_users_db = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@router.get("/", response_model=List[UserRead])
def get_user():
    return [{k: v for k, v in user.items() if k != "password"} for user in fake_users_db]

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate):
    new_id = max(user["id"] for user in fake_users_db) + 1 if fake_users_db else 1
    hashed_pw = hash_password(user.password)
    new_user = {
        "id": new_id,
        "name": user.name,
        "email": user.email,
        "password": hashed_pw

    }
    fake_users_db.append(new_user)
    return {k: v for k, v in new_user.items() if k != "password"}

@router.post("/login", response_model=Token)
def login(user: UserLogin):
    matched_user = next((u for u in fake_users_db if u["email"] == user.email), None)
    if not matched_user or not verify_password(user.password, matched_user["password"]):
        raise HTTPException(status_code=401, detail="잘못된 이메일 또는 비밀번호입니다.")

    token = create_access_token({"sub": matched_user["email"]})
    return {
        "access_token": token,
          "token_type": "bearer"
    }

@router.get("/protected")
def protected_route(request: Request):
    auth: str = request.headers.get("authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    
    token = auth.split(" ")[1]
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=403, detail="토큰이 유효하지 않습니다.")

    return {
        "message": f"인증 성공 {payload['sub']}님 환영합니다."
    }
