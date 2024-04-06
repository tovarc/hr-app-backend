from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import database
from api.models import models
from api.schemas import schemas

from api.utils.auth import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

get_db = database.get_db


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Positions],
)
async def get_all_positions(db: Session = Depends(get_db)):
    employees = db.query(models.Positions).all()
    return employees


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Positions,
)
async def create_position(
    position: schemas.CreatePosition, db: Session = Depends(get_db)
):
    new_position = models.Positions(
        name=position.name,
        responsibilities=position.responsibilities,
        min_salary=position.min_salary,
        max_salary=position.max_salary,
    )
    db.add(new_position)
    db.commit()
    db.refresh(new_position)
    return new_position


@router.patch("", status_code=status.HTTP_200_OK, response_model=schemas.Positions)
async def update_positon(positionn: schemas.Positions, db: Session = Depends(get_db)):
    db_position = (
        db.query(models.Positions).filter(models.Positions.id == positionn.id).first()
    )

    if db_position:
        for key, value in positionn:
            setattr(db_position, key, value)

        db.commit()
        db.refresh(db_position)
        return db_position
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Position with ID: {positionn.id} does not exist.",
        )


@router.delete("/{position_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_position(position_id: int, db: Session = Depends(get_db)):
    db_position = (
        db.query(models.Positions).filter(models.Positions.id == position_id).first()
    )

    if db_position:
        db.delete(db_position)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Position with ID: {position_id} does not exist.",
        )
