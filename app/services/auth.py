# app/services/auth.py

from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.jwt import verify_access_token

# 보안 스키마 선언
bearer_scheme = HTTPBearer()

# 더미 유저 DB
fake_users_db = [
    {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "password": "hashed2",
        "bio": "Hello, I'm Alice!",
        "profile_image_url": None,
        "followers": [],
        "following": []
    },
    {
        "id": 2,
        "name": "Bob",
        "email": "bob@example.com",
        "password": "hashed1",
        "bio": "Hello, I'm Bob!",
        "profile_image_url": None,
        "followers": [],
        "following": []
    }
]

# 현재 로그인된 사용자 가져오기
def get_current_user(
    token: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    token_str = token.credentials  # 실제 Bearer 토큰 문자열

    payload = verify_access_token(token_str)
    if not payload:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    user_email = payload.get("sub")
    user = next((u for u in fake_users_db if u["email"] == user_email), None)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    return user
