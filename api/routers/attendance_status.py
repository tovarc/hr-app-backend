from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from api.database import database
from api.models import models
from api.schemas import schemas


router = APIRouter()

get_db = database.get_db


def get_attendance_status(id: int, db: Session):
    attendance_status = db.get(models.AttendanceStatus, id)
    return attendance_status


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_attendance_status(db: Session = Depends(get_db)):
    attendance_status = db.query(models.AttendanceStatus).all()

    return attendance_status


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_attendance_status(
    attendance_status: schemas.CreateAttendanceStatus, db: Session = Depends(get_db)
):
    new_attendance_status = models.AttendanceStatus(**attendance_status.model_dump())
    db.add(new_attendance_status)
    db.commit()
    db.refresh(new_attendance_status)
    return new_attendance_status


#
# @router.patch("", status_code=status.HTTP_200_OK)
# async def update_attendance(
#     attendance: schemas.UpdateLeaveRequest, db: Session = Depends(get_db)
# ):
#     db_leave_request = get_leave_request(attendance.id, db)
#
#     if db_leave_request:
#         for key, value in attendance:
#             setattr(db_leave_request, key, value)
#
#         db.commit()
#         db.refresh(db_leave_request)
#         return db_leave_request
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Employee with ID: {attendance.id} does not exist.",
#         )


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
