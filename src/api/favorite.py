from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.db_models import Checklist, Favorite, User
from src.schemas import ChecklistListResponse, ChecklistResponse
from src.core.dependencies import get_current_user

router = APIRouter(tags=["favorites"])


def get_checklist_or_404(checklist_id: int, db: Session) -> Checklist:
    checklist = db.query(Checklist).filter(Checklist.id == checklist_id).first()
    if not checklist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Checklist not found")
    return checklist


@router.post("/api/checklists/{checklist_id}/favorites", status_code=status.HTTP_201_CREATED)
def add_favorite(
    checklist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_checklist_or_404(checklist_id, db)

    existing = db.query(Favorite).filter(
        Favorite.checklist_id == checklist_id,
        Favorite.user_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already in favorites")

    favorite = Favorite(checklist_id=checklist_id, user_id=current_user.id)
    db.add(favorite)

    checklist = get_checklist_or_404(checklist_id, db)
    checklist.saves_count += 1

    db.commit()


@router.delete("/api/checklists/{checklist_id}/favorites", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    checklist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_checklist_or_404(checklist_id, db)

    favorite = db.query(Favorite).filter(
        Favorite.checklist_id == checklist_id,
        Favorite.user_id == current_user.id
    ).first()
    if not favorite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not in favorites")

    db.delete(favorite)

    checklist = get_checklist_or_404(checklist_id, db)
    checklist.saves_count -= 1

    db.commit()


@router.get("/api/users/me/favorites", response_model=ChecklistListResponse)
def get_my_favorites(
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total = db.query(Favorite).filter(Favorite.user_id == current_user.id).count()

    favorites = db.query(Favorite).filter(
        Favorite.user_id == current_user.id
    ).offset((page - 1) * size).limit(size).all()

    checklists = [
        db.query(Checklist).filter(Checklist.id == f.checklist_id).first()
        for f in favorites
    ]

    return ChecklistListResponse(
        checklists=checklists,
        total=total,
        page=page,
        size=size,
        has_prev=page > 1,
        has_next=(page * size) < total
    )