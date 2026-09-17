from fastapi import FastAPI
from api.v1 import learn1, learn2, learn3, learn4

app = FastAPI(title="Learn FastAPI...")

# 统一再挂一层 /api/v1 版本前缀
app.include_router(learn1.router, prefix="/api/v1")
app.include_router(learn2.router, prefix="/api/v1")
app.include_router(learn3.router, prefix="/api/v1")
app.include_router(learn4.router, prefix="/api/v1")
