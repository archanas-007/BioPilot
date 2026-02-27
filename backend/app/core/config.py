from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "BioPilot"
    ENVIRONMENT: str = "dev"
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str

    MINIO_ENDPOINT: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    S3_BUCKET_NAME: str

    REDIS_URL: str
    QDRANT_URL: str

    OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
