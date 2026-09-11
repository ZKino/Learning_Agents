from fastapi import FastAPI
from api.v1 import items, users

app = FastAPI(title="fastapi_02")

# 统一再挂一层 /api/v1 版本前缀
app.include_router(items.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
