from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.models.user import UserModel


class RoleCheck:
    def __init__(self, allow_roles: list[str]):
        self.allow_roles = allow_roles

    def __call__(self,user_data: UserModel = Depends(get_current_user)):
        if user_data.role not in self.allow_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền truy cập tài nguyên này"
            )

        return user_data