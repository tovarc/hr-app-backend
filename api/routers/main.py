from fastapi import APIRouter
from api.routers import (
    auth,
    attendance,
    attendance_status,
    employees,
    departments,
    positions,
    leave_requests,
    leave_requests_status,
)

api_router = APIRouter()

api_router.include_router(prefix="/auth", router=auth.router, tags=["Login / Register"])

api_router.include_router(
    prefix="/employees", router=employees.router, tags=["Employees"]
)
api_router.include_router(
    prefix="/departments", router=departments.router, tags=["Departments"]
)
api_router.include_router(
    prefix="/positions", router=positions.router, tags=["Positions"]
)
api_router.include_router(
    prefix="/leave-requests", router=leave_requests.router, tags=["Leave Requests"]
)
api_router.include_router(
    prefix="/leave-requests-status",
    router=leave_requests_status.router,
    tags=["Leave Requests Status"],
)
api_router.include_router(
    prefix="/attendances",
    router=attendance.router,
    tags=["Attendance"],
)
api_router.include_router(
    prefix="/attendance-status",
    router=attendance_status.router,
    tags=["Attendance Status"],
)
