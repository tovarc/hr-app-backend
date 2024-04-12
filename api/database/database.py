from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from api.core.settings import settings


DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()


# Accessing to database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
