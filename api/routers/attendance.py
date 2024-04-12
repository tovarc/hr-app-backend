from functools import partial
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from api.database import database
from api.models import models
from api.schemas import schemas


from api.utils.auth import get_current_user, get_user_roles

router = APIRouter()

get_db = database.get_db


def get_attendance(id: int, db: Session):
    attendance = db.get(models.Attendance, id)
    return attendance


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_attendances(db: Session = Depends(get_db)):
    attendances = (
        db.query(models.Attendance)
        .options(
            joinedload(models.Attendance.status),
            joinedload(models.Attendance.employee),
        )
        .all()
    )

    return attendances


@router.get(
    "/current-employee",
    dependencies=[Depends(partial(get_user_roles, ["employee"]))],
    status_code=status.HTTP_200_OK,
)
async def get_all_current_employee_attendances(
    user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)
):
    attendances = (
        db.query(models.Attendance)
        .where(models.Attendance.employee_id == user.employee.id)
        .options(
            joinedload(models.Attendance.status),
            joinedload(models.Attendance.employee),
        )
        .all()
    )

    return attendances


@router.post(
    "/employee",
    dependencies=[Depends(partial(get_user_roles, ["employee"]))],
    status_code=status.HTTP_201_CREATED,
)
async def create_attendance_by_employee(
    attendance: schemas.CreateAttendanceByEmployee,
    user: schemas.User = Depends(partial(get_user_roles, ["employee"])),
    db: Session = Depends(get_db),
):
    new_attendance = models.Attendance(**attendance.model_dump())
    setattr(new_attendance, "employee_id", user.employee.id)

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_attendance(
    attendance: schemas.CreateAttendance, db: Session = Depends(get_db)
):
    new_attendance = models.Attendance(**attendance.model_dump())
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    return new_attendance


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
