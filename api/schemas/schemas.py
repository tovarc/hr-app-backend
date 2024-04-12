from datetime import datetime, time
from pydantic import BaseModel


class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    role_id: int
    employee_id: int


class UserLogin(BaseModel):
    email: str
    password: str


class Role(BaseModel):
    id: int
    name: str


class UpdateUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    role_id: int
    employee_id: int


class Employees(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    position_id: int
    department_id: int
    hire_date: datetime


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    password: str
    role: Role
    employee: Employees


class AssignEmployee(BaseModel):
    user_id: int
    employee_id: int


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


class CreateDepartment(BaseModel):
    name: str


class Positions(BaseModel):
    id: int
    name: str
    responsibilities: str
    min_salary: float
    max_salary: float


class CreatePosition(BaseModel):
    name: str
    responsibilities: str
    min_salary: float
    max_salary: float


class EmployeesResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    position: Positions
    department: Departments
    hire_date: datetime


class CreateLeaveRequest(BaseModel):
    employee_id: int
    start_date: datetime
    end_date: datetime
    reason: str
    status_id: int


class CreateLeaveRequestByEmployee(BaseModel):
    start_date: datetime
    end_date: datetime
    reason: str


class UpdateLeaveRequest(BaseModel):
    id: int
    start_date: datetime
    end_date: datetime
    reason: str
    employee_id: int
    status_id: int


class LeaveRequestsStatus(BaseModel):
    id: int
    name: str


class CreateLeaveRequestStatus(BaseModel):
    name: str


class UpdateLeaveRequestStatus(BaseModel):
    id: int
    name: str


class LeaveRequestsResponse(BaseModel):
    id: int
    employee_id: int
    start_date: datetime
    end_date: datetime
    reason: str
    status: LeaveRequestsStatus
    employee: Employees


class AttendanceStatus(BaseModel):
    id: int
    name: str


class CreateAttendanceStatus(BaseModel):
    name: str


class CreateAttendance(BaseModel):
    employee_id: int
    date: datetime
    time_in: time
    time_out: time
    status_id: int


class CreateAttendanceByEmployee(BaseModel):
    date: datetime
    time_in: time
    time_out: time
    status_id: int


class AttendanceResponse(BaseModel):
    id: int
    employee: Employees
    date: datetime
    time_in: datetime
    time_out: datetime
    status: AttendanceStatus
    employee: Employees
