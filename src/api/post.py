from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.db_models import Post, ChecklistItem, User
from src.schemas import PostCreate, PostResponse, PostUpdate, PostListResponse
from src.core.dependencies import get_current_user

router = APIRouter(prefix="/api/posts", tags=["posts"])


def get_post_or_404(post_id: int, db: Session) -> Post:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.query(ChecklistItem).filter(ChecklistItem.id == data.item_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Checklist item not found")

    new_post = Post(
        image_url=str(data.image_url),
        description=data.description,
        user_id=current_user.id,
        item_id=data.item_id,
        likes_count=0,
        comments_count=0
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=PostListResponse)
def get_posts(
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db)
):
    total = db.query(Post).count()
    posts = db.query(Post).order_by(Post.created_at.desc()).offset((page - 1) * size).limit(size).all()

    return PostListResponse(
        posts=posts,
        total=total,
        page=page,
        size=size,
        has_prev=page > 1,
        has_next=(page * size) < total
    )


@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    return get_post_or_404(post_id, db)


@router.patch("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    data: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = get_post_or_404(post_id, db)

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your post")

    if data.description is not None:
        post.description = data.description

    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = get_post_or_404(post_id, db)

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your post")

    db.delete(post)
    db.commit()


@router.get("/user/{user_id}", response_model=PostListResponse)
def get_user_posts(
    user_id: int,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    total = db.query(Post).filter(Post.user_id == user_id).count()
    posts = db.query(Post).filter(
        Post.user_id == user_id
    ).order_by(Post.created_at.desc()).offset((page - 1) * size).limit(size).all()

    return PostListResponse(
        posts=posts,
        total=total,
        page=page,
        size=size,
        has_prev=page > 1,
        has_next=(page * size) < total
    )