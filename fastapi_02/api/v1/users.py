from fastapi import APIRouter

# prefix: 该模块所有路由的统一前缀
# tags: /docs 中的分组标题
router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_users():
    return [{"name": "Tracy"}]
    # 实际路径: GET /users/


@router.get("/{id}")
def get_user(id: int):
    return {"id": id}
    # 实际路径: GET /users/{id}
