from passlib.context import CryptContext
from api.models import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.core.settings import settings


DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI
#
# engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
#


engine = create_engine(
    "postgresql://hr_app_iafa_user:CBnRTPzHsJh2fiLnWCaxSzzqpNbR2P75@dpg-co6b3v8l6cac73a6fsj0-a.oregon-postgres.render.com/hr_app_iafa"
)
SessionLocal = sessionmaker(autoflush=False, bind=engine)


db = SessionLocal()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def seed_database():
    roles = ["admin", "employee"]
    for role in roles:
        db.add(models.Role(name=role))

    db.commit()
    print("Roles added sucessfully...")

    admin_role = db.query(models.Role).filter(models.Role.name == "admin").first()

    if admin_role:
        admin = models.User(
            first_name="admin",
            last_name="admin",
            email="admin@admin.com",
            password=get_password_hash("admin"),
            role_id=admin_role.id,
        )

        db.add(admin)
        db.commit()
        print("Admin added sucessfully...")

    leave_requests_status = ["Pending", "Approved", "Denied"]

    for status in leave_requests_status:
        db.add(models.LeaveRequestsStatus(name=status))

    db.commit()
    print("Leave Requests status added successfully...")

    attendances_status = ["Present", "Absent", "Late"]

    for status in attendances_status:
        db.add(models.AttendanceStatus(name=status))

    db.commit()
    print("Attendances status added successfully...")


seed_database()
