from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.role import RoleCheck
from app.models.user import UserModel
from app.schemas.user import UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me",response_model=UserResponse)
def get_my_profile(current_user: UserModel = Depends(get_current_user)):
    return current_user


@router.get("/",response_model=list[UserResponse])
def get_all_users(current_user: UserModel = Depends(RoleCheck(["ADMIN"])),db: Session = Depends(get_db)):
    return db.query(UserModel).all()