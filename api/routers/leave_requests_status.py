from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import database
from api.models import models
from api.schemas import schemas


router = APIRouter()

get_db = database.get_db


def get_leave_request_status(id: int, db: Session):
    leave_request_status = db.get(models.LeaveRequestsStatus, id)
    return leave_request_status


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_leave_requests_status(db: Session = Depends(get_db)):
    leave_requests_status = db.query(models.LeaveRequestsStatus).all()

    return leave_requests_status


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_leave_request_status(
    leave_request_status: schemas.CreateLeaveRequestStatus,
    db: Session = Depends(get_db),
):
    new_leave_request = models.LeaveRequestsStatus(**leave_request_status.model_dump())
    db.add(new_leave_request)
    db.commit()
    db.refresh(new_leave_request)
    return new_leave_request


@router.patch("", status_code=status.HTTP_200_OK)
async def update_leave_request_status(
    leave_request_status: schemas.UpdateLeaveRequestStatus,
    db: Session = Depends(get_db),
):
    db_leave_request_status = get_leave_request_status(leave_request_status.id, db)

    if db_leave_request_status:
        for key, value in leave_request_status:
            setattr(db_leave_request_status, key, value)

        db.commit()
        db.refresh(db_leave_request_status)
        return db_leave_request_status
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID: {leave_request_status.id} does not exist.",
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
