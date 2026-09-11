from fastapi import APIRouter

# prefix: 该模块所有路由的统一前缀
# tags: /docs 中的分组标题
router = APIRouter(prefix="/items", tags=["商品"])


@router.get("/")
async def get_items():
    return [{"name": "键盘"}]


@router.get("/{id}")
async def get_item(id: int):
    return {"id": id}
