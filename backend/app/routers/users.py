from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("", response_model=schemas.UserOut, status_code=201)
def register_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.phone == payload.phone).first()
    if existing:
        return existing  # idempotent onboarding: re-registering just returns the account
    user = models.User(name=payload.name, phone=payload.phone)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user
