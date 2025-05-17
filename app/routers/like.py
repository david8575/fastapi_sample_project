from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.post_like import Like
from app.models.user import User
from app.services.auth import get_current_user
from app.schemas.like import LikeCreate

router = APIRouter(prefix="/like", tags=["Like"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def like_post(like_data: LikeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.post_id == like_data.post_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="already liked")
    
    like = Like(user_id=current_user.id, post_id=like_data.post_id)
    db.add(like)
    db.commit()
    
    return {
        "message": "Liked"
    }