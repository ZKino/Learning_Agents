from typing import Annotated
from fastapi import APIRouter, Path

# prefix: 该模块所有路由的统一前缀
# tags: /docs 中的分组标题
router = APIRouter(prefix="/learn1", tags=["learn1"])


# **************************************路劲参数**************************************
@router.get("/items/{id}")
async def get_item(id: Annotated[int, Path(ge=1, le=100, description="1-100之间的ID")]):
    return {"id": id, "id_type": type(id).__name__}
