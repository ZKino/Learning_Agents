from typing import Annotated
from pydantic import BaseModel, Field, HttpUrl
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
