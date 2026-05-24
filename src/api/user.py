from fastapi import APIRouter, Depends
from src.schemas import UserResponse
from src.core.dependencies import get_current_user
from src.db_models import User

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user
