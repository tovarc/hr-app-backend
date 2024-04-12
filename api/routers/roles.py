from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from api.database import database
from api.models import models
from api.utils.auth import get_user_roles
from functools import partial

router = APIRouter()

get_db = database.get_db


@router.get(
    "",
    dependencies=[Depends(partial(get_user_roles, ["admin"]))],
    status_code=status.HTTP_200_OK,
)
async def get_all_roles(
    db: Session = Depends(get_db),
):
    roles = db.query(models.Role).all()

    return roles
