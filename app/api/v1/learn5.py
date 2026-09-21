import re
from typing import Annotated

from fastapi import APIRouter
from pydantic import AfterValidator, BaseModel, BeforeValidator

# prefix: 该模块所有路由的统一前缀
# tags: /docs 中的分组标题
router = APIRouter(prefix="/learn5", tags=["learn5"])


# 可复用校验：Annotated 类型别名
def _validata_phone(v: str) -> str:
    if not re.fullmatch(r"1[3-9]\d{9}", v):
        raise ValueError("手机号格式不正确")
    return v


def _strip_str(v) -> str:
    return v.strip() if isinstance(v, str) else v


# 手机号：先校验格式
PhoneStr = Annotated[str, AfterValidator(_validata_phone)]

# 自动去空格 + 长度约束的通用字符串
StrippedStr = Annotated[str, BeforeValidator(_strip_str)]

# 复用方式：像普通类型一样标注
class AddressCreate(BaseModel):
    contact_name: StrippedStr
    contact_phone: PhoneStr
    detail: StrippedStr
