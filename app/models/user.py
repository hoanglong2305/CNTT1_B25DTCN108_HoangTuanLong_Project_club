from sqlalchemy import Column, Integer, String ,Boolean, DateTime
from app.db.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable= False)
    full_name = Column(String(25), nullable= False)
    role = Column(String(10), default="USER", nullable=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    owned_clubs = relationship("ClubModel", back_populates="owner", cascade="all, delete-orphan")
    club_memberships = relationship("MemberModel", back_populates="user", cascade="all, delete-orphan")
    assigned_activities = relationship("ActivityModel", back_populates="assignee")