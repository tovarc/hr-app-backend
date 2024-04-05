from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:temporal123@localhost:5432/hr_app"
# DATABASE_URL = "postgresql://hr_app_iafa_user:CBnRTPzHsJh2fiLnWCaxSzzqpNbR2P75@dpg-co6b3v8l6cac73a6fsj0-a.oregon-postgres.render.com/hr_app_iafa"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()


# Accessing to database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
