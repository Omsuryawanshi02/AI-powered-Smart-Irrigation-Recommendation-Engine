from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..utils import to_hectares, estimate_growth_stage, estimate_season

router = APIRouter(prefix="/api/fields", tags=["fields"])


@router.post("", response_model=schemas.FieldOut, status_code=201)
def create_field(payload: schemas.FieldCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).get(payload.user_id)
    if not user:
        raise HTTPException(404, "User not found")

    field = models.Field(
        user_id=payload.user_id,
        name=payload.name,
        crop_type=payload.crop_type,
        crop_growth_stage=payload.crop_growth_stage or estimate_growth_stage(payload.sowing_date),
        sowing_date=payload.sowing_date,
        field_area_hectare=to_hectares(payload.field_size, payload.size_unit),
        soil_type=payload.soil_type or "Loamy",
        region=payload.region or "Central",
        season=payload.season or estimate_season(),
        irrigation_type=payload.irrigation_type or "Drip",
        water_source=payload.water_source or "Groundwater",
        mulching_used=bool(payload.mulching_used),
        latitude=payload.latitude,
        longitude=payload.longitude,
    )
    db.add(field)
    db.commit()
    db.refresh(field)
    return field


@router.get("", response_model=List[schemas.FieldOut])
def list_fields(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(models.Field)
    if user_id is not None:
        q = q.filter(models.Field.user_id == user_id)
    return q.order_by(models.Field.created_at.desc()).all()


@router.get("/{field_id}", response_model=schemas.FieldOut)
def get_field(field_id: int, db: Session = Depends(get_db)):
    field = db.query(models.Field).get(field_id)
    if not field:
        raise HTTPException(404, "Field not found")
    return field


@router.put("/{field_id}", response_model=schemas.FieldOut)
def update_field(field_id: int, payload: schemas.FieldUpdate, db: Session = Depends(get_db)):
    field = db.query(models.Field).get(field_id)
    if not field:
        raise HTTPException(404, "Field not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(field, key, value)

    db.commit()
    db.refresh(field)
    return field


@router.delete("/{field_id}", status_code=204)
def delete_field(field_id: int, db: Session = Depends(get_db)):
    field = db.query(models.Field).get(field_id)
    if not field:
        raise HTTPException(404, "Field not found")
    db.delete(field)
    db.commit()
    return None
