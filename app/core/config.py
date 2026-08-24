from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Student Club Management API"
    VERSION: str = "1.0.0"
    
    DATABASE_URL: str = "mysql+pymysql://root:123456@localhost:3306/club_management_db"
    
    SECRET_KEY: str = "sdajhbdsabchsbcssdajhbdsabchsbcs"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()