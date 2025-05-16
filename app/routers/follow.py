from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.follow import Follow
from app.models.user import User
from app.schemas.follow import FollowCreate, FollowRead
from app.services.auth import get_current_user

router = APIRouter(prefix="/follow", tags=["Follow"])

@router.post("/", response_model=FollowRead, status_code=status.HTTP_201_CREATED)
def follow_user(follow: FollowCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.id == follow.following_id:
        raise HTTPException(status_code=400, detail="you cannot follow yourself")

    existing = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.following_id == follow.following_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="already following")

    new_follow = Follow(
        follower_id=current_user.id,
        following_id=follow.following_id
    )
    db.add(new_follow)
    db.commit()
    db.refresh(new_follow)
    return new_follow

@router.delete("/{following_id}", status_code=status.HTTP_204_NO_CONTENT)
def unfollow_user(following_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    follow = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.following_id == following_id
    ).first()

    if not follow:
        raise HTTPException(status_code=404, detail="follow relationship not found")

    db.delete(follow)
    db.commit()
