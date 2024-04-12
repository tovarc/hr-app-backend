from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from api.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="user")

    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    employee = relationship("Employees", back_populates="user")


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    user = relationship("User", back_populates="role")


class Employees(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    position_id = Column(Integer, ForeignKey("positions.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    hire_date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="employee")
    position = relationship("Positions", back_populates="employees")
    department = relationship("Departments", back_populates="employees")
    attendance = relationship("Attendance", back_populates="employee")
    leave_request = relationship("LeaveRequests", back_populates="employee")


class Departments(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    employees = relationship("Employees", back_populates="department")


class Positions(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    responsibilities = Column(String, nullable=False)
    min_salary = Column(Float, nullable=False)
    max_salary = Column(Float, nullable=False)

    employees = relationship("Employees", back_populates="position")


class LeaveRequests(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    reason = Column(String, nullable=False, default="No reason")
    status_id = Column(Integer, ForeignKey("leave_requests_status.id"))

    status = relationship("LeaveRequestsStatus", back_populates="leave_request")
    employee = relationship("Employees", back_populates="leave_request")


class LeaveRequestsStatus(Base):
    __tablename__ = "leave_requests_status"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    leave_request = relationship("LeaveRequests", back_populates="status")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    date = Column(DateTime, nullable=False)
    time_in = Column(Time, nullable=False)
    time_out = Column(Time, nullable=False)
    status_id = Column(Integer, ForeignKey("attendance_status.id"))

    employee = relationship("Employees", back_populates="attendance")
    status = relationship("AttendanceStatus", back_populates="attendance")


class AttendanceStatus(Base):
    __tablename__ = "attendance_status"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    attendance = relationship("Attendance", back_populates="status")
