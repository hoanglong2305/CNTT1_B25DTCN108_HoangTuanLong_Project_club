
from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import HTTPException, status
from app.models.user import UserModel
from app.models.club import ClubModel
from app.models.club_member import MemberModel
from app.schemas.club import ClubMemberResponse, ClubBase, ClubResponse, ClubMemberCreate, ClubMemberBase, ClubUpdate


def handle_get_club(db: Session, current_user_id: int, name: Optional[str] = None):
    query = (db.query(ClubModel).outerjoin(MemberModel, ClubModel.id == MemberModel.club_id).filter((ClubModel.owner_id == current_user_id) | (MemberModel.user_id == current_user_id)))
    if name:
        query = query.filter(ClubModel.name.ilike(f"%{name}%"))

    return query.distinct().all()

def handle_create_club(db: Session, club_data: ClubBase, current_user_id: int) -> ClubModel:
    new_club = ClubModel(
        name=club_data.name,
        description=club_data.description,
        owner_id=current_user_id
    )
    db.add(new_club)
    db.flush()

    new_member = MemberModel(
        club_id=new_club.id,
        user_id=current_user_id,
        role="OWNER"
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_club)
    
    return new_club

def handle_get_club_by_id(db: Session, club_id: int, current_user_id: int) -> ClubModel:
    club = db.query(ClubModel).filter(ClubModel.id == club_id).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Câu lạc bộ không tồn tại"
        )

    is_member = (db.query(MemberModel).filter(MemberModel.club_id == club_id, MemberModel.user_id == current_user_id).first())
    if not is_member and club.owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xem thông tin câu lạc bộ này"
        )

    return club

def handle_update_club(db: Session, club_id: int, club_data: ClubUpdate, current_user_id: int) -> ClubModel:
    club = db.query(ClubModel).filter(ClubModel.id == club_id).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Câu lạc bộ không tồn tại"
        )
    if club.owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới có quyền chỉnh sửa câu lạc bộ"
        )

    if club_data.name is not None:
        club.name = club_data.name
    if club_data.description is not None:
        club.description = club_data.description

    db.commit()
    db.refresh(club)
    return club

def handle_delete_club(db: Session, club_id: int, current_user_id: int):
    club = db.query(ClubModel).filter(ClubModel.id == club_id).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Câu lạc bộ không tồn tại"
        )

    if club.owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới có quyền xóa câu lạc bộ"
        )

    db.query(MemberModel).filter(MemberModel.club_id == club_id).delete()
    db.delete(club)
    db.commit()
    return {"message": "Xóa câu lạc bộ thành công"}

def handle_add_member(db: Session, club_id: int, member_data: ClubMemberCreate, current_user_id: int):
    club = db.query(ClubModel).filter(ClubModel.id == club_id).first()
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Câu lạc bộ không tồn tại")

    if club.owner_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ OWNER mới có quyền thêm thành viên")

    target_user = db.query(UserModel).filter(UserModel.id == member_data.user_id).first()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Người dùng không tồn tại")

    existed_member = (db.query(MemberModel).filter(MemberModel.club_id == club_id, MemberModel.user_id == member_data.user_id).first())
    if existed_member:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Người dùng đã là thành viên của câu lạc bộ")

    new_member = MemberModel(
        club_id=club_id,
        user_id=member_data.user_id,
        role=getattr(member_data, "role", "MEMBER")
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

def handle_remove_member(db: Session, club_id: int, target_user_id: int, current_user_id: int):
    club = db.query(ClubModel).filter(ClubModel.id == club_id).first()
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Câu lạc bộ không tồn tại")

    if club.owner_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Chỉ OWNER mới có quyền xóa thành viên")

    member_to_remove = (db.query(MemberModel).filter(MemberModel.club_id == club_id, MemberModel.user_id == target_user_id).first())
    if not member_to_remove:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thành viên không tồn tại trong câu lạc bộ")

    if member_to_remove.role == "OWNER" or target_user_id == club.owner_id:
        owner_count = (db.query(MemberModel).filter(MemberModel.club_id == club_id, MemberModel.role == "OWNER").count())
        if not owner_count:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Không thể xóa OWNER duy nhất của câu lạc bộ"
            )

    db.delete(member_to_remove)
    db.commit()
    return {"message": "Xóa thành viên thành công"}

def handle_get_members(db: Session, club_id: int, current_user_id: int):
    club = db.query(ClubModel).filter(ClubModel.id == club_id).first()
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Câu lạc bộ không tồn tại")

    return db.query(MemberModel).filter(MemberModel.club_id == club_id).all()