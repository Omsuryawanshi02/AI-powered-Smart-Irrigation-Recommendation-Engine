from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api", tags=["alerts"])


@router.get("/fields/{field_id}/alerts", response_model=List[schemas.AlertOut])
def list_field_alerts(field_id: int, unread_only: bool = False, limit: int = 50, db: Session = Depends(get_db)):
    field = db.query(models.Field).get(field_id)
    if not field:
        raise HTTPException(404, "Field not found")

    q = db.query(models.Alert).filter(models.Alert.field_id == field_id)
    if unread_only:
        q = q.filter(models.Alert.is_read.is_(False))
    return q.order_by(models.Alert.created_at.desc()).limit(limit).all()


@router.get("/users/{user_id}/alerts", response_model=List[schemas.AlertOut])
def list_user_alerts(user_id: int, unread_only: bool = False, limit: int = 50, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(404, "User not found")

    field_ids = [f.id for f in user.fields]
    q = db.query(models.Alert).filter(models.Alert.field_id.in_(field_ids))
    if unread_only:
        q = q.filter(models.Alert.is_read.is_(False))
    return q.order_by(models.Alert.created_at.desc()).limit(limit).all()


@router.patch("/alerts/{alert_id}/read", response_model=schemas.AlertOut)
def mark_alert_read(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(models.Alert).get(alert_id)
    if not alert:
        raise HTTPException(404, "Alert not found")
    alert.is_read = True
    db.commit()
    db.refresh(alert)
    return alert


@router.delete("/alerts/{alert_id}", status_code=204)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(models.Alert).get(alert_id)
    if not alert:
        raise HTTPException(404, "Alert not found")
    db.delete(alert)
    db.commit()
    return None
