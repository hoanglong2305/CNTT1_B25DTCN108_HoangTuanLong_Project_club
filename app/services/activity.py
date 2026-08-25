from enum import Enum
from typing import Optional, Tuple, List
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from fastapi import HTTPException, status

from app.models import ActivityModel, ClubModel, MemberModel, UserModel
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityStatus, ActivityPriority


def check_club_membership(club_id: int, user_id: int, db: Session) -> bool:
    is_owner = db.query(ClubModel).filter(ClubModel.id == club_id, ClubModel.owner_id == user_id).first()
    if is_owner:
        return True
        
    is_member = db.query(MemberModel).filter(MemberModel.club_id == club_id, MemberModel.user_id == user_id).first()
    return is_member is not None

def get_activity_detail(activity_id: int,current_user: UserModel,db: Session) -> ActivityModel:
    activity = (db.query(ActivityModel).filter(ActivityModel.id == activity_id).first())

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hoạt động"
        )
        
    if not check_club_membership(activity.club_id,current_user.id,db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xem hoạt động này"
        )

    return activity

def create_activity(club_id: int, payload: ActivityCreate, current_user: UserModel, db: Session) -> ActivityModel:
    club = db.query(ClubModel).filter(ClubModel.id == club_id).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Không tìm thấy câu lạc bộ"
        )
        
    if payload.assignee_id is not None:

        if not check_club_membership(club_id, current_user.id, db):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Bạn không có quyền tạo hoạt động trong câu lạc bộ này"
            )

    new_activity = ActivityModel(
        club_id=club_id,
        title=payload.title,
        description=payload.description,
        due_date=payload.due_date,
        priority=payload.priority.value,
        status=ActivityStatus.TODO.value,
        assignee_id=payload.assignee_id
    )
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity

def update_activity(activity_id: int,payload: ActivityUpdate,current_user: UserModel,db: Session) -> ActivityModel:
    activity = (db.query(ActivityModel).filter(ActivityModel.id == activity_id).first())
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hoạt động"
        )

    club = (db.query(ClubModel).filter(ClubModel.id == activity.club_id).first())

    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy câu lạc bộ của hoạt động"
        )

    is_owner = club.owner_id == current_user.id
    is_assignee = activity.assignee_id == current_user.id
    is_member = check_club_membership(activity.club_id,current_user.id,db)

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải thành viên của câu lạc bộ"
        )

    update_data = payload.model_dump(exclude_unset=True)

    if is_owner:
        allowed_fields = {
            "title",
            "description",
            "due_date",
            "priority",
            "status",
            "assignee_id"
        }
    elif is_assignee:
        allowed_fields = {
            "status"
        }
    else:
        allowed_fields = set()
        
    for field in update_data:
        if field not in allowed_fields:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền cập nhật trường"
            )

    if "assignee_id" in update_data:
        target_user_id = update_data["assignee_id"]
        if target_user_id is not None:

            if not check_club_membership(
                activity.club_id,
                target_user_id,
                db
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Người được giao phải là thành viên của câu lạc bộ này"
                )

    for field, value in update_data.items():
        setattr(activity, field, getattr(value, "value", value))

    db.commit()
    db.refresh(activity)

    return activity

def get_activities_by_club(
    club_id: int,
    current_user: UserModel,
    db: Session,
    status_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    assignee_id: Optional[int] = None,
    search: Optional[str] = None,
    page: int = 1,
    size: int = 10,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> Tuple[int, List[ActivityModel]]:

    club = (db.query(ClubModel).filter(ClubModel.id == club_id).first())

    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy câu lạc bộ"
        )

    if not check_club_membership(club_id,current_user.id,db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xem hoạt động của câu lạc bộ này"
        )

    query = (db.query(ActivityModel).filter(ActivityModel.club_id == club_id))

    if status_filter:
        query = query.filter(ActivityModel.status == status_filter)

    if priority_filter:
        query = query.filter(ActivityModel.priority == priority_filter)

    if assignee_id is not None:
        query = query.filter(ActivityModel.assignee_id == assignee_id)

    if search:
        query = query.filter(ActivityModel.title.ilike(f"%{search}%"))

    total = query.count()
    order_column = getattr(ActivityModel, sort_by)

    if sort_order == "desc":
        query = query.order_by(desc(order_column))
    else:
        query = query.order_by(asc(order_column))

    items = (query.offset((page - 1) * size).limit(size).all())
    return total, items

def delete_activity(activity_id: int,current_user: UserModel,db: Session) -> None:
    activity = (db.query(ActivityModel).filter(ActivityModel.id == activity_id).first())

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy hoạt động"
        )

    club = (db.query(ClubModel).filter(ClubModel.id == activity.club_id).first())

    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy câu lạc bộ"
        )

    if club.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới có thể xóa hoạt động"
        )

    db.delete(activity)
    db.commit()