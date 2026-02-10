import urllib.parse
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # --- Project Metadata ---
    PROJECT_NAME: str = "KSHRD Certificate Verify Service"
    DEBUG: bool = True

    # --- Database Variables ---
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str

    # --- Keycloak Configuration ---
    KEYCLOAK_URL: str
    KEYCLOAK_REALM: str
    KEYCLOAK_CLIENT_ID: str
    # Usually needed if your Keycloak client is set to 'confidential'
    KEYCLOAK_CLIENT_SECRET: str | None = None

    # --- Redis Configuration ---
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def REDIS_URL(self) -> str:
        """Constructs the async redis URL for the connection pool"""
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def DATABASE_URL(self) -> str:
        encoded_pw = urllib.parse.quote_plus(self.DB_PASSWORD)
        return f"postgresql+asyncpg://{self.DB_USER}:{encoded_pw}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def JWKS_URL(self) -> str:
        """The URL where your API finds the public keys to verify JWT signatures."""
        return f"{self.KEYCLOAK_URL}/realms/{self.KEYCLOAK_REALM}/protocol/openid-connect/certs"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
