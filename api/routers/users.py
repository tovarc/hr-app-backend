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


def get_user(id: int, db: Session):
    user = db.get(models.User, id)
    return user


@router.get(
    "",
    dependencies=[Depends(partial(get_user_roles, ["admin"]))],
    status_code=status.HTTP_200_OK,
)
async def get_all_users(
    db: Session = Depends(get_db),
):
    users = (
        db.query(models.User)
        .options(joinedload(models.User.employee), joinedload(models.User.role))
        .all()
    )

    return users


#
# @router.post(
#     "",
#     dependencies=[Depends(partial(get_user_roles, ["admin"]))],
#     response_model=schemas.Employees,
#     status_code=status.HTTP_201_CREATED,
# )
# async def create_employee(
#     employee: schemas.CreateEmployee, db: Session = Depends(get_db)
# ):
#     new_employee = models.Employees(**employee.model_dump())
#     db.add(new_employee)
#     db.commit()
#     db.refresh(new_employee)
#     return new_employee
#
#


@router.patch(
    "",
    dependencies=[Depends(partial(get_user_roles, ["admin"]))],
    status_code=status.HTTP_200_OK,
)
async def update_user(user: schemas.UpdateUser, db: Session = Depends(get_db)):
    db_user = get_user(user.id, db)

    if db_user:
        for key, value in user:
            setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID: {user.id} does not exist.",
        )


#
# @router.delete(
#     "/{employee_id}",
#     dependencies=[Depends(partial(get_user_roles, ["admin"]))],
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# async def delete_employee(employee_id: int, db: Session = Depends(get_db)):
#     db_employee = get_employee(employee_id, db)
#
#     if db_employee:
#         db.delete(db_employee)
#         db.commit()
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Employee with ID: {employee_id} does not exist.",
#         )
