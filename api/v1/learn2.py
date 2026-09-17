from typing import Annotated
from fastapi import APIRouter, Query

# prefix: 该模块所有路由的统一前缀
# tags: /docs 中的分组标题
router = APIRouter(prefix="/learn2", tags=["learn2"])


# **************************************查询参数**************************************
# 实际路径: GET /learn2?page=1&size=20&keywords=abc&tag=py&tag=js
@router.get("")
async def get_items(
    page: Annotated[int, Query(ge=1, description="页码")] = 1,
    size: Annotated[int, Query(ge=10, le=100, description="条码")] = 20,
    keywords: Annotated[
        str | None, Query(min_length=1, max_length=50, description="关键词")
    ] = None,
    tag: Annotated[list[str], Query(description="标签")] = None,
):
    return {"page": page, "size": size, "keywords": keywords, "tag": tag}
