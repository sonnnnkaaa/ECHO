from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserResponse