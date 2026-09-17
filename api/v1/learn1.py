from enum import Enum
from typing import Annotated

from fastapi import APIRouter, Path

# prefix: 该模块所有路由的统一前缀
# tags: /docs 中的分组标题
router = APIRouter(prefix="/learn1", tags=["learn1"])


# **************************************路劲参数**************************************
@router.get("/items1/{id}")
async def get_item1(id: int):
    return {"id": id, "id_type": type(id).__name__}


@router.get("/items2/{id}")
async def get_item2(
    id: Annotated[int, Path(ge=1, le=100, description="1-100之间的ID")],
):
    return {"id": id, "id_type": type(id).__name__}


@router.get("/items3/{id}")
async def get_item3(id: Annotated[str, Path(pattern=r"^a\d{2}")]):
    """正则 a开头后2位数字"""
    return {"id": id, "id_type": type(id).__name__}


class NameEnum(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@router.get("/items4/{name}")
async def get_item4(name: NameEnum):
    return {"name": name}
