from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.models import UserModel
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityResponse, ActivityListResponse, ActivityStatus, ActivityPriority
from app.dependencies.auth import get_current_user
import app.services.activity as activity_service

router = APIRouter(tags=["Club Activities"])


@router.post("/clubs/{club_id}/activities", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
def create_activity(
    club_id: int,
    payload: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return activity_service.create_activity(
        club_id=club_id, 
        payload=payload, 
        current_user=current_user, 
        db=db
    )


@router.get("/activities/{activity_id}", response_model=ActivityResponse)
def get_activity_detail(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return activity_service.get_activity_detail(
        activity_id=activity_id, 
        current_user=current_user, 
        db=db
    )
    
@router.get("/clubs/{club_id}/activities", response_model=ActivityListResponse)
def get_club_activities(
    club_id: int,
    status_filter: Optional[str] = Query(None, alias="status", pattern="^(TODO|IN_PROGRESS|DONE)$"),
    priority_filter: Optional[str] = Query(None, alias="priority", pattern="^(LOW|MEDIUM|HIGH)$"),
    assignee_id: Optional[int] = Query(None, alias="assignee_id"),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    sort_by: str = Query("created_at", pattern="^(created_at|due_date)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    total, items = activity_service.get_activities_by_club(
        club_id=club_id,
        current_user=current_user,
        db=db,
        status_filter=status_filter,
        priority_filter=priority_filter,
        assignee_id=assignee_id,
        search=search,
        page=page,
        size=size,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return {"total": total, "items": items}

@router.patch("/activities/{activity_id}", response_model=ActivityResponse)
def update_activity(
    activity_id: int,
    payload: ActivityUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return activity_service.update_activity(
        activity_id=activity_id, 
        payload=payload, 
        current_user=current_user, 
        db=db
    )


@router.delete("/activities/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    activity_service.delete_activity(
        activity_id=activity_id, 
        current_user=current_user, 
        db=db
    )
    return None