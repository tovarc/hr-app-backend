from fastapi import APIRouter

from api.routers import employees, departments, positions


api_router = APIRouter()


api_router.include_router(
    prefix="/employees", router=employees.router, tags=["Employees"]
)
api_router.include_router(
    prefix="/departments", router=departments.router, tags=["Departments"]
)
api_router.include_router(
    prefix="/positions", router=positions.router, tags=["Positions"]
)
