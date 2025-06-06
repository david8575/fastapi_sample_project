from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.post import Post
from app.models.user import User
from app.models.follow import Follow
from app.models.post import Post
from app.schemas.post import PostCreate, PostRead
from app.services.auth import get_current_user
from typing import List


router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_post = Post(
        user_id = current_user.id,
        content = post.content,
        image_url = post.image_url 
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/feed", response_model=List[PostRead])
def get_feed(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    following = db.query(Follow.follower_id).filter(
        Follow.follower_id == current_user.id
    ).subquery()

    psots = db.query(Post).filter(Post.user_id.in_(following)).order_by(Post.id.desc()).all()
