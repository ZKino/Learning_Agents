from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 声明即文档：每行一个配置项，带类型和默认值
    APP_NAME: str = "Learn FastAPI..."
    DEBUG: bool = True
    SECRET_KEY: str = "dev-only-change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    DATABASE_URL: str = (
        "mysql+aiomysql://root:root123456@localhost:3306/my_test_01?charset=utf8"
    )

    # v2 配置：从 .env 读取，环境变量优先；大小写不敏感
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="uft-8",
        extra="ignore",
    )


@lru_cache  # 全进程只解析一次
def get_settings() -> Settings:
    return Settings()
