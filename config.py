from pydantic.v1 import BaseSettings

class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    ACCESS_TOKEN_EXPIRES_IN:int=30
    JWT_ALGORITHM:str
    JWT_PRIVATE_KEY:str

    class Config:
        env_file = '.env'


settings = Settings()