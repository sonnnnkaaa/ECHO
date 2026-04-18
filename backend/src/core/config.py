from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "some_db_url"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    TOKEN_ALGORITHM: str = "HS256"
    PASS_SCHEMES: list = ["pbkdf2_sha512", "md5_crypt"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    class Config:
        env_file = ".env"

    
settings = Settings()
    