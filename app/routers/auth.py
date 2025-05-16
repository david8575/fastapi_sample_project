from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserLogin, Token
from app.services.hash import verify_password
from app.services.jwt import create_access_token

router = APIRouter(prefix="/login", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(user_cred: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_cred.email).first()

    if not user or not verify_password(user_cred.password, user.password):
        raise HTTPException(status_code=401, detail="invalid credentials")
    
    token = create_access_token(data={
        "sub":user.email
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }