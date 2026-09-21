from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

# prefix: 该模块所有路由的统一前缀
# tags: /docs 中的分组标题
router = APIRouter(prefix="/learn7", tags=["learn7"])


# 依赖注入


# 一个普通函数：声明它"提供什么"，内部可以做任何逻辑
def pagination(offset: int = 0, limit: int = 0) -> tuple[int, int]:
    if limit > 100:
        raise HTTPException(status_code=400, detail="limit不能超过100")
    return offset, limit


# 用 Depends 声明"我需要 pagination 的产物"
PaginationDep = Annotated[tuple[int, int], Depends(pagination)]


@router.get("/items")
async def list_items(page: PaginationDep):
    offset, limit = page
    return {"offset": offset, "limit": limit, "data": []}


@router.get("/users")
async def list_users(page: PaginationDep):
    offset, limit = page
    return {"offset": offset, "limit": limit, "data": []}


class ArticleFilter:
    def __init__(
        self,
        category: str | None = None,
        tag: str | None = None,
        keyword: str | None = None,
        offset: int = 1,
        limit: int = 10,
    ):
        self.category = category
        self.tag = tag
        self.keyword = keyword
        self.offset = offset
        self.limit = limit


@router.get("/articles")
async def list_articles(f: Annotated[ArticleFilter, Depends(ArticleFilter)]):
    return {"filters": f.__dict__}
