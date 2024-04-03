from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from api.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


class Employees(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    position_id = Column(Integer, ForeignKey("positions.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    hire_date = Column(DateTime, nullable=False)

    position = relationship("Positions", back_populates="employees")
    department = relationship("Departments", back_populates="employees")


class Departments(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    employees = relationship("Employees", back_populates="department")


class Positions(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    responsibilities = Column(String, nullable=False)
    min_salary = Column(Float, nullable=False)
    max_salary = Column(Float, nullable=False)

    employees = relationship("Employees", back_populates="position")
