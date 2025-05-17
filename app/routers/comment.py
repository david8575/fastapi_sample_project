from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.comment import Comment
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentRead
from app.services.auth import get_current_user

router = APIRouter(prefix="/comment", tags=["Comment"])

@router.post("/", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_comment = Comment(
        user_id=current_user.id,
        post_id=comment.post_id,
        content=comment.content
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
