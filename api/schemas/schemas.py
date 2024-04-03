from datetime import datetime
from pydantic import BaseModel


class Employees(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    position_id: int
    department_id: int
    hire_date: datetime


class CreateEmployee(BaseModel):
    first_name: str
    last_name: str
    email: str
    position_id: int
    department_id: int
    hire_date: datetime


class Departments(BaseModel):
    id: int
    name: str


class Positions(BaseModel):
    id: int
    name: str
    responsibilities: str
    min_salary: float
    max_salary: float
