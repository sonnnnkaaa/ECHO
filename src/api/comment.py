from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.db_models import Post, Comment, User
from src.schemas import CommentCreate, CommentResponse, CommentUpdate, CommentListResponse
from src.core.dependencies import get_current_user

router = APIRouter(prefix="/api/posts/{post_id}/comments", tags=["comments"])


def get_post_or_404(post_id: int, db: Session) -> Post:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


def get_comment_or_404(comment_id: int, post_id: int, db: Session) -> Comment:
    comment = db.query(Comment).filter(
        Comment.id == comment_id,
        Comment.post_id == post_id
    ).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = get_post_or_404(post_id, db)

    comment = Comment(
        text=data.content,
        post_id=post_id,
        author_id=current_user.id
    )
    db.add(comment)

    post.comments_count += 1

    db.commit()
    db.refresh(comment)
    return comment


@router.get("/", response_model=CommentListResponse)
def get_comments(
    post_id: int,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db)
):
    get_post_or_404(post_id, db)

    total = db.query(Comment).filter(Comment.post_id == post_id).count()
    comments = db.query(Comment).filter(
        Comment.post_id == post_id
    ).order_by(Comment.created_at.desc()).offset((page - 1) * size).limit(size).all()

    return CommentListResponse(
        comments=comments,
        total=total,
        page=page,
        size=size,
        has_prev=page > 1,
        has_next=(page * size) < total
    )


@router.patch("/{comment_id}", response_model=CommentResponse)
def update_comment(
    post_id: int,
    comment_id: int,
    data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_post_or_404(post_id, db)
    comment = get_comment_or_404(comment_id, post_id, db)

    if comment.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your comment")

    if data.content is not None:
        comment.text = data.content

    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = get_post_or_404(post_id, db)
    comment = get_comment_or_404(comment_id, post_id, db)

    if comment.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your comment")

    db.delete(comment)
    post.comments_count -= 1
    db.commit()