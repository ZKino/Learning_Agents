import re
from typing import Annotated
from typing_extensions import Self
from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    EmailStr,
    field_validator,
    model_validator,
)
from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/")
async def root():
    return {"msg": "Hello World..."}


# 路径参数 https://xxx.com/items/10
@app.get("/items/{id}")
async def get_item(id: Annotated[int, Path(title="item id", ge=1, le=100)]):
    return {"id": id, "id_type": type(id).__name__}


# 查询参数 https://xxx.com/books?page=1&size=20&keywords=abc&tag=py&tag=js
@app.get("/books/")
async def get_books(
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
    keywords: Annotated[
        str | None,
        Query(
            title="search keywords",
            min_length=1,
            max_length=50,
            description="input your keywords",
        ),
    ] = None,
    tag: Annotated[list[str] | None, Query()] = None,
):
    return {"page": page, "size": size, "keywords": keywords, "tag": tag}


# 请求体参数
class Image(BaseModel):
    id: int = Field(ge=1)
    url: HttpUrl
    name: str = Field(max_length=100)


class Seller(BaseModel):
    id: int = Field(ge=1)
    nickname: str = Field(min_length=1, max_length=20)


class Goods(BaseModel):
    id: int = Field(ge=1)
    name: str = Field(min_length=1, max_length=50)
    price: float = Field(gt=0)
    tags: list[str] = Field(default_factory=list, max_length=10)
    images: list[Image] = Field(default_factory=list)
    seller: Seller


@app.post("/create/goods")
async def create_goods(goods: Goods):
    return {
        "goods_name": goods.name,
        "seller_nickname": goods.seller.nickname,
        "images_count": len(goods.images),
    }


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


@app.post("/user/register", response_model=UserResponse)
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


@app.post("/user/register2", response_model=UserResponse2)
def user_register(user: UserRegister2):
    return user
