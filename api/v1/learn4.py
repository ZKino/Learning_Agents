import re
from typing_extensions import Self
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from fastapi import APIRouter

# prefix: 该模块所有路由的统一前缀
# tags: /docs 中的分组标题
router = APIRouter(prefix="/learn4", tags=["learn4"])


# field_validator：单字段自定义校验
class UserRegister1(BaseModel):
    username: str = Field(min_length=1, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

    @field_validator("username")
    @classmethod
    def normalize_username(cls, v: str) -> str:
        # 1. 清洗：去除首尾空格
        v = v.strip()
        # 2. 业务规则：只允许字母、数字、下划线
        if not re.fullmatch(r"[a-zA-Z0-9_]+", v):
            raise ValueError("用户名只能包含字母、数字和下划线")
        # 3. 返回处理后的值（校验器可以"改写"数据）
        return v.lower()

    @field_validator("password")
    @classmethod
    def check_password_strength(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("密码必须包含至少一个大写字母")
        if not re.search(r"[0-9]", v):
            raise ValueError("密码必须包含至少一个数字")
        return v


class UserResponse(BaseModel):
    username: str
    email: EmailStr


@router.post("/user/register", response_model=UserResponse)
def user_register(user: UserRegister1):
    return user


# model_validator：跨字段联合校验
class UserRegister2(BaseModel):
    username: str = Field(min_length=1, max_length=20)
    password: str = Field(min_length=8)
    password_confirm: str = Field(min_length=8)

    @model_validator(mode="after")
    def password_match(self) -> Self:
        if self.password != self.password_confirm:
            raise ValueError("两次输入的密码不一致")
        return self


class UserResponse2(BaseModel):
    username: str


@router.post("/user/register2", response_model=UserResponse2)
def user_register(user: UserRegister2):
    return user
