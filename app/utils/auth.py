from app.models.user import UserModel
from app.core.security import handle_hash_password


def handle_register_service(user_account, db):
    user = db.query(UserModel).filter(UserModel.username == user_account.username).first()
    if user:
        return "Tên Tài Khoản Đã Tồn Tại"

    hash_password = handle_hash_password(user_account.password)

    new_account = UserModel(username=..., password=hash_password, email=..., role_id=3)
    db.add(new_account); db.commit(); db.refresh(new_account)
    return new_account