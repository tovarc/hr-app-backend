from functools import partial
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from api.database import database
from api.models import models
from api.schemas import schemas

from api.utils.auth import get_user_roles

router = APIRouter()
get_db = database.get_db


def get_leave_request(id: int, db: Session):
    leave_request = db.get(models.LeaveRequests, id)
    return leave_request


@router.get(
    "",
    dependencies=[Depends(partial(get_user_roles, ["admin", "employee"]))],
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.LeaveRequestsResponse],
)
async def get_all_leave_requests(db: Session = Depends(get_db)):
    leave_requests = (
        db.query(models.LeaveRequests)
        .options(joinedload(models.LeaveRequests.status))
        .all()
    )

    return leave_requests


@router.get(
    "/current-employee",
    dependencies=[Depends(partial(get_user_roles, ["employee"]))],
    status_code=status.HTTP_200_OK,
)
async def get_all_current_employee_leave_requests(
    user: schemas.User = Depends(partial(get_user_roles, ["employee"])),
    db: Session = Depends(get_db),
):
    leave_requests = (
        db.query(models.LeaveRequests)
        .where(models.LeaveRequests.employee_id == user.employee.id)
        .options(
            joinedload(models.LeaveRequests.status),
            joinedload(models.LeaveRequests.employee),
        )
        .all()
    )

    return leave_requests


@router.post(
    "",
    dependencies=[Depends(partial(get_user_roles, ["admin"]))],
    status_code=status.HTTP_201_CREATED,
)
async def create_leave_request(
    leave_request: schemas.CreateLeaveRequest, db: Session = Depends(get_db)
):
    new_leave_request = models.LeaveRequests(**leave_request.model_dump())
    db.add(new_leave_request)
    db.commit()
    db.refresh(new_leave_request)
    return new_leave_request


@router.post(
    "/employee",
    dependencies=[Depends(partial(get_user_roles, ["employee"]))],
    status_code=status.HTTP_201_CREATED,
)
async def create_leave_request_by_employee(
    leave_request: schemas.CreateLeaveRequestByEmployee,
    user: schemas.User = Depends(partial(get_user_roles, ["employee"])),
    db: Session = Depends(get_db),
):
    pending_status = (
        db.query(models.LeaveRequestsStatus)
        .filter(models.LeaveRequestsStatus.name == "Pending")
        .first()
    )

    if pending_status:
        new_leave_request = models.LeaveRequests(**leave_request.model_dump())
        setattr(new_leave_request, "employee_id", user.employee.id)
        setattr(new_leave_request, "status_id", pending_status.id)
        db.add(new_leave_request)
        db.commit()
        db.refresh(new_leave_request)
        return new_leave_request


@router.patch(
    "",
    dependencies=[Depends(partial(get_user_roles, ["admin"]))],
    status_code=status.HTTP_200_OK,
)
async def update_leave_request(
    leave_request: schemas.UpdateLeaveRequest, db: Session = Depends(get_db)
):
    db_leave_request = get_leave_request(leave_request.id, db)

    if db_leave_request:
        for key, value in leave_request:
            setattr(db_leave_request, key, value)

        db.commit()
        db.refresh(db_leave_request)
        return db_leave_request
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID: {leave_request.id} does not exist.",
        )


#
# @router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_employee(employee_id: int, db: Session = Depends(get_db)):
#     db_employee = get_leave_request(employee_id, db)
#
#     if db_employee:
#         db.delete(db_employee)
#         db.commit()
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Employee with ID: {employee_id} does not exist.",
#         )
