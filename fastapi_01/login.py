from typing import Annotated
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException, status, security
import jwt
from pwdlib import PasswordHash

# 演示密钥（HS256 要求 ≥32 字节；生产用 openssl rand -hex 32 并放环境变量）
SECRET_KEY = "dev-only-secret-key-at-least-32-bytes!"
ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    return jwt.encode({"sub": subject, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


# —— 模拟用户库（密码是 "Secret123" 的哈希）——
fake_users = {
    "tom": {
        "id": 1,
        "username": "tom",
        "role": "admin",
        "hashed_password": password_hash.hash("Secret123"),
    }
}


# —— Schemas ——
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    username: str
    role: str


# ——实例FastAPI——
app = FastAPI()

# tokenUrl 指向登录接口，让 Swagger UI 的 Authorize 按钮知道去哪换令牌
oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exc
    except jwt.PyJWTError:
        raise credentials_exc

    user = fake_users.get(username)

    if user is None:
        raise credentials_exc
    return user


CurrentUser = Annotated[dict, Depends(get_current_user)]


# —— 接口 ——
@app.post("/auth/login", response_model=Token)
async def login(form: Annotated[security.OAuth2PasswordRequestForm, Depends()]):
    """OAuth2 标准登录：接收 form-data 的 username/password"""
    user = fake_users.get(form.username)
    if user is None or not password_hash.verify(form.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )
    return Token(access_token=create_access_token(subject=user["username"]))


@app.get("/auth/me", response_model=UserOut)
def read_me(user: CurrentUser):
    return user
