from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.db_models import Checklist, ChecklistCategory, User
from src.schemas import ChecklistCreate, ChecklistResponse, ChecklistUpdate, ChecklistListResponse
from src.core.dependencies import get_current_user

router = APIRouter(prefix="/api/checklists", tags=["checklists"])


def get_checklist_or_404(checklist_id: int, db: Session) -> Checklist:
    checklist = db.query(Checklist).filter(Checklist.id == checklist_id).first()
    if not checklist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Checklist not found")
    return checklist


@router.post("/", response_model=ChecklistResponse, status_code=status.HTTP_201_CREATED)
def create_checklist(
    data: ChecklistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    categories = db.query(ChecklistCategory).filter(ChecklistCategory.title.in_(data.categories)).all()

    new_checklist = Checklist(
        title=data.title,
        description=data.description,
        image_url=str(data.image_url) if data.image_url else None,
        author_id=current_user.id,
        saves_count=0,
        categories=categories
    )
    db.add(new_checklist)
    db.commit()
    db.refresh(new_checklist)
    return new_checklist


@router.get("/", response_model=ChecklistListResponse)
def get_checklists(
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db)
):
    total = db.query(Checklist).count()
    checklists = db.query(Checklist).offset((page - 1) * size).limit(size).all()

    return ChecklistListResponse(
        checklists=checklists,
        total=total,
        page=page,
        size=size,
        has_prev=page > 1,
        has_next=(page * size) < total
    )


@router.get("/{checklist_id}", response_model=ChecklistResponse)
def get_checklist(
    checklist_id: int,
    db: Session = Depends(get_db)
):
    return get_checklist_or_404(checklist_id, db)


@router.patch("/{checklist_id}", response_model=ChecklistResponse)
def update_checklist(
    checklist_id: int,
    data: ChecklistUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    checklist = get_checklist_or_404(checklist_id, db)

    if checklist.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your checklist")

    if data.title is not None:
        checklist.title = data.title
    if data.image_url is not None:
        checklist.image_url = str(data.image_url)
    if data.categories is not None:
        checklist.categories = db.query(ChecklistCategory).filter(
            ChecklistCategory.title.in_(data.categories)
        ).all()

    db.commit()
    db.refresh(checklist)
    return checklist


@router.delete("/{checklist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_checklist(
    checklist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    checklist = get_checklist_or_404(checklist_id, db)