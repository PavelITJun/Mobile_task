from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        """
        A computed property that returns the full database URI.

        Examples:
            - postgresql+asyncpg://user:pass@localhost:5432/dbname

        Returns:
            str: The full database URI.
        """
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@\
{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def TEST_DATABASE_URL(self):
        """
        A computed property that returns the full test database URI.

        Examples:
            - postgresql+asyncpg://user:pass@localhost:5432/dbname

        Returns:
            str: The full test database URI.
        """
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@\
{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
