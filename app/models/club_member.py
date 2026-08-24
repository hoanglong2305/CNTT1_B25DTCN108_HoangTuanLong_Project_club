from app.db.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class MemberModel(Base):
    __tablename__ = "club_members"

    club_id = Column(Integer, ForeignKey("clubs.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(String(10), nullable=True)
    joined_at = Column(DateTime,default=datetime.utcnow ,nullable=False)

    club = relationship("ClubModel", back_populates="members")
    user = relationship("UserModel", back_populates="club_memberships")