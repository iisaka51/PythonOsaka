from pydantic import BaseSettings

class Settings(BaseSettings):
    database_uri: str

    class Config:
        env_file = '.env'
        case_sensitive = False

settings = Settings()
print(settings.database_uri)
