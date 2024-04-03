from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import database
from api.models import models
from api.schemas import schemas


router = APIRouter()

get_db = database.get_db


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Departments],
)
async def get_all_departments(db: Session = Depends(get_db)):
    departments = db.query(models.Departments).all()
    return departments


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Departments,
)
async def create_department(
    department: schemas.CreateDepartment, db: Session = Depends(get_db)
):
    new_department = models.Departments(**department.model_dump())
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department


@router.patch("", status_code=status.HTTP_200_OK, response_model=schemas.Departments)
async def update_department(
    department: schemas.Departments, db: Session = Depends(get_db)
):
    db_department = (
        db.query(models.Departments)
        .filter(models.Departments.id == department.id)
        .first()
    )

    if db_department:
        for key, value in department:
            setattr(db_department, key, value)

        db.commit()
        db.refresh(db_department)
        return db_department
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with ID: {department.id} does not exist.",
        )


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(department_id: int, db: Session = Depends(get_db)):
    db_department = (
        db.query(models.Departments)
        .filter(models.Departments.id == department_id)
        .first()
    )

    if db_department:
        db.delete(db_department)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with ID: {department_id} does not exist.",
        )
