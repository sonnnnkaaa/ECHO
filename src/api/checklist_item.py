from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.db_models import Checklist, ChecklistItem, User
from src.schemas import ChecklistItemCreate, ChecklistItemResponse, ChecklistItemUpdate, ChecklistItemListResponse
from src.core.dependencies import get_current_user

router = APIRouter(prefix="/api/checklists/{checklist_id}/items", tags=["checklist items"])


def get_checklist_or_404(checklist_id: int, db: Session) -> Checklist:
    checklist = db.query(Checklist).filter(Checklist.id == checklist_id).first()
    if not checklist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Checklist not found")
    return checklist


def get_item_or_404(item_id: int, checklist_id: int, db: Session) -> ChecklistItem:
    item = db.query(ChecklistItem).filter(
        ChecklistItem.id == item_id,
        ChecklistItem.checklist_id == checklist_id
    ).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.post("/", response_model=ChecklistItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    checklist_id: int,
    data: ChecklistItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    checklist = get_checklist_or_404(checklist_id, db)

    if checklist.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your checklist")

    last_item = db.query(ChecklistItem).filter(
        ChecklistItem.checklist_id == checklist_id
    ).order_by(ChecklistItem.order_number.desc()).first()

    next_order = (last_item.order_number + 1) if last_item else 1

    new_item = ChecklistItem(
        description=data.description,
        order_number=next_order,
        checklist_id=checklist_id
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.get("/", response_model=ChecklistItemListResponse)
def get_items(
    checklist_id: int,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db)
):
    get_checklist_or_404(checklist_id, db)

    total = db.query(ChecklistItem).filter(ChecklistItem.checklist_id == checklist_id).count()
    items = db.query(ChecklistItem).filter(
        ChecklistItem.checklist_id == checklist_id
    ).order_by(ChecklistItem.order_number).offset((page - 1) * size).limit(size).all()

    return ChecklistItemListResponse(
        checklist_items=items,
        total=total,
        page=page,
        size=size,
        has_prev=page > 1,
        has_next=(page * size) < total
    )


@router.patch("/{item_id}", response_model=ChecklistItemResponse)
def update_item(
    checklist_id: int,
    item_id: int,
    data: ChecklistItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    checklist = get_checklist_or_404(checklist_id, db)

    if checklist.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your checklist")

    item = get_item_or_404(item_id, checklist_id, db)
    item.description = data.description

    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    checklist_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    checklist = get_checklist_or_404(checklist_id, db)

    if checklist.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your checklist")

    item = get_item_or_404(item_id, checklist_id, db)
    db.delete(item)
    db.commit()