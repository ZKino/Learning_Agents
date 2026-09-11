from fastapi import APIRouter

# prefix: 该模块所有路由的统一前缀
# tags: /docs 中的分组标题
router = APIRouter(prefix="/items", tags=["items"])


@router.get("/")
def get_items():
    return [{"name": "键盘"}]
    # 实际路径: GET /items/


@router.get("/{id}")
def get_item(id: int):
    return {"id": id}
    # 实际路径: GET /items/{id}
