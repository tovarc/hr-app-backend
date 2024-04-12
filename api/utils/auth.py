from typing import Annotated, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session, joinedload

from api.core.settings import settings
from api.database import database
from api.models import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

get_db = database.get_db


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        db_user = (
            db.query(models.User)
            .options(joinedload(models.User.role), joinedload(models.User.employee))
            .get(payload.get("id"))
        )

        if db_user:
            return db_user
        else:
            raise credentials_exception
    except JWTError:
        raise credentials_exception


def get_user_roles(
    roles: List[str],
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        db_user = (
            db.query(models.User)
            .options(joinedload(models.User.role))
            .get(payload.get("id"))
        )

        if db_user and db_user.role.name in roles:
            return db_user
        else:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
