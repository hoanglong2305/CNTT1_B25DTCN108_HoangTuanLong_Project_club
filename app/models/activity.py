from app.db.database import Base
from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class ActivityModel(Base):
    __tablename__ = "club_activities"
    
    id = Column(Integer, primary_key= True)
    club_id = Column(Integer, ForeignKey("clubs.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(25), nullable=False)
    priority = Column(String(25), nullable=False)
    
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    club = relationship("ClubModel", back_populates="activities")
    assignee = relationship("UserModel", back_populates="assigned_activities")