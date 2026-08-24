from fastapi import FastAPI, HTTPException
from app.core.config import settings
from app.db.database import engine, Base

from app.models.user import UserModel
from app.models.club import ClubModel
from app.models.club_member import MemberModel
from app.models.activity import ActivityModel

from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.club import router as clubs_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(clubs_router)

@app.get("/health", tags=["Health Check"])
def health_check():
    return {
        "message": "XIN CHÀO"
    }