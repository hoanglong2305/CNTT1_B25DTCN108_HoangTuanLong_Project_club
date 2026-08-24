from app.db.database import Base
from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class ClubModel(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    owner = relationship("UserModel", back_populates="owned_clubs")
    members = relationship("MemberModel", back_populates="club", cascade="all, delete-orphan")
    activities = relationship("ActivityModel", back_populates="club", cascade="all, delete-orphan")


