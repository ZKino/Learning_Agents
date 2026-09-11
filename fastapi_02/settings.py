from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 声明即文档：每行一个配置项，带类型和默认值
    APP_NAME: str = "fastapi 02"
    DEBUG: bool = False
    SECRET_KEY: str = "dev-only-change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    DATABASE_URL: str = "sqlite+aiosqlite:///./blog.db"
    REDIS_URL: str = "redis://localhost:6379/0"

    # v2 配置：从 .env 读取，环境变量优先；大小写不敏感
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache  # 全进程只解析一次
def get_settings() -> Settings:
    return Settings()
