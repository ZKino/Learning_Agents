from fastapi import FastAPI

from app.api.v1 import learn1, learn2, learn3, learn4, learn5, learn6, learn7
from app.core.config import get_settings


def create_lifespan(settings):
    async def lifespan(app: FastAPI):
        # 启动时：初始化连接池等
        print(f"🚀 {settings.APP_NAME} starting, DEBUG={settings.DEBUG}")
        yield
        # 关闭时：释放资源
        print("👋 shutting down")

    return lifespan


def create_app() -> FastAPI:
    settings = get_settings()
    title = settings.APP_NAME
    debug = settings.DEBUG
    lifespan = create_lifespan(settings)
    app = FastAPI(title=title, debug=debug, lifespan=lifespan)

    # 统一再挂一层 /api/v1 版本前缀
    app.include_router(learn1.router, prefix="/api/v1")
    app.include_router(learn2.router, prefix="/api/v1")
    app.include_router(learn3.router, prefix="/api/v1")
    app.include_router(learn4.router, prefix="/api/v1")
    app.include_router(learn5.router, prefix="/api/v1")
    app.include_router(learn6.router, prefix="/api/v1")
    app.include_router(learn7.router, prefix="/api/v1")

    @app.get("/health", tags=["运维"])
    def health():
        return {"status": "ok"}

    return app


app = create_app()
