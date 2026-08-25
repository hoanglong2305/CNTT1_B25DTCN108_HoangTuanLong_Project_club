from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.role import RoleCheck
from app.models.user import UserModel
from app.models.club import ClubModel
from app.schemas.club import ClubUpdate
from app.models.club_member import MemberModel
from app.schemas.club import ClubBase,ClubMemberBase,ClubMemberCreate,ClubMemberResponse,ClubResponse
from app.services.club import handle_get_club, handle_create_club, handle_get_club_by_id, handle_update_club, handle_delete_club, handle_add_member, handle_remove_member, handle_get_members


router = APIRouter(
    prefix="/clubs",
    tags=["Clubs"]
)



@router.get("", response_model=List[ClubResponse])
def get_clubs(name: Optional[str] = Query(None, description="Tìm kiếm câu lạc bộ theo tên"),db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    return handle_get_club(db=db, current_user_id=current_user.id, name=name)

@router.post("", response_model=ClubResponse, status_code=status.HTTP_201_CREATED)
def create_club(club_data: ClubBase,db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    return handle_create_club(db=db, club_data=club_data, current_user_id=current_user.id)

@router.get("/{id}", response_model=ClubResponse)
def get_club_detail(id: int,db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    return handle_get_club_by_id(db=db, club_id=id, current_user_id=current_user.id)

@router.patch("/{id}", response_model=ClubResponse)
def update_club(id: int,club_data: ClubUpdate,db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    return handle_update_club(db=db, club_id=id, club_data=club_data, current_user_id=current_user.id)

@router.delete("/{id}")
def delete_club(id: int,db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    return handle_delete_club(db=db, club_id=id, current_user_id=current_user.id)

@router.post("/{id}/members", status_code=status.HTTP_201_CREATED)
def add_member(id: int,member_data: ClubMemberCreate,db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    return handle_add_member(db=db, club_id=id, member_data=member_data, current_user_id=current_user.id)

@router.delete("/{id}/members/{user_id}")
def remove_member(id: int,user_id: int,db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    return handle_remove_member(db=db, club_id=id, target_user_id=user_id, current_user_id=current_user.id)

@router.get("/{id}/members", response_model=List[ClubMemberResponse])
def get_members(id: int,db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    return handle_get_members(db=db, club_id=id, current_user_id=current_user.id)