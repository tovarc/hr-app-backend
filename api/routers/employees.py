from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from api.database import database
from api.models import models
from api.schemas import schemas
from api.utils.auth import get_user_roles
from functools import partial

router = APIRouter()

get_db = database.get_db


def get_employee(id: int, db: Session):
    employee = db.get(models.Employees, id)
    return employee


@router.get(
    "",
    dependencies=[Depends(partial(get_user_roles, ["admin"]))],
    response_model=List[schemas.EmployeesResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_employees(
    db: Session = Depends(get_db),
):
    employees = (
        db.query(models.Employees).options(joinedload(models.Employees.position)).all()
    )

    return employees


@router.post(
    "",
    dependencies=[Depends(partial(get_user_roles, ["admin"]))],
    response_model=schemas.Employees,
    status_code=status.HTTP_201_CREATED,
)
async def create_employee(
    employee: schemas.CreateEmployee, db: Session = Depends(get_db)
):
    new_employee = models.Employees(**employee.model_dump())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


@router.patch(
    "",
    dependencies=[Depends(partial(get_user_roles, ["admin"]))],
    status_code=status.HTTP_200_OK,
    response_model=schemas.Employees,
)
async def update_employee(employee: schemas.Employees, db: Session = Depends(get_db)):
    db_employee = get_employee(employee.id, db)

    if db_employee:
        for key, value in employee:
            setattr(db_employee, key, value)

        db.commit()
        db.refresh(db_employee)
        return db_employee
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID: {employee.id} does not exist.",
        )


@router.delete(
    "/{employee_id}",
    dependencies=[Depends(partial(get_user_roles, ["admin"]))],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = get_employee(employee_id, db)

    if db_employee:
        db.delete(db_employee)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID: {employee_id} does not exist.",
        )
