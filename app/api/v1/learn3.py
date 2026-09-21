from fastapi import APIRouter
from pydantic import BaseModel, Field, HttpUrl

# prefix: 该模块所有路由的统一前缀
# tags: /docs 中的分组标题
router = APIRouter(prefix="/learn3", tags=["learn3"])


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


# **************************************请求体参数**************************************
@router.post("/create/goods")
async def create_goods(goods: Goods):
    return {
        "goods_name": goods.name,
        "seller_nickname": goods.seller.nickname,
        "images_count": len(goods.images),
    }
