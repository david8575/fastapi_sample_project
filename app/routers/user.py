from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from app.schemas.user import UserCreate, UserRead, UserLogin, UserUpdate
from app.schemas.token import Token
from app.services.security import hash_password, verify_password
from app.services.jwt import create_access_token, verify_access_token
from app.services.auth import get_current_user, fake_users_db

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

@router.get("/me", response_model=UserRead)
def read_my_profile(current_user: dict = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserRead)
def update_my_profile(update: UserUpdate, current_user: dict = Depends(get_current_user)):
    for k, v in update.dict(exclude_unset=True).items():
        current_user[k] = v

    return current_user

@router.post("/{user_id}/follow")
def follow_user(user_id: int, current_user: dict = Depends(get_current_user)):
    target = next((u for u in fake_users_db if u["id"] == user_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="팔로우 대상 사용자를 찾을 수 없음")

    if target["id"] == current_user["id"]:
        raise HTTPException(status_code=400, detail="자기 자신은 팔로우할 수 없음")

    if current_user["id"] not in target["followers"]:
        target["followers"].append(current_user["id"])
    if target["id"] not in current_user["following"]:
        current_user["following"].append(target["id"])

    return {"message": f"{target['name']}님을 팔로우"}

@router.delete("/{user_id}/unfollow")
def unfollow_user(user_id: int, current_user: dict = Depends(get_current_user)):
    target = next((u for u in fake_users_db if u["id"] == user_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="언팔로우 대상 사용자를 찾을 수 없음")

    if current_user["id"] in target["followers"]:
        target["followers"].remove(current_user["id"])
    if target["id"] in current_user["following"]:
        current_user["following"].remove(target["id"])

    return {"message": f"{target['name']}님을 언팔로우"}

@router.get("/me/following")
def get_following(current_user: dict = Depends(get_current_user)):
    following = [u for u in fake_users_db if u["id"] in current_user["following"]]
    return following

@router.get("/me/followers")
def get_followers(current_user: dict = Depends(get_current_user)):
    followers = [u for u in fake_users_db if current_user["id"] in u["following"]]
    return followers