from fastapi import APIRouter
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    StreamingResponse,
)
from pydantic import BaseModel, EmailStr

# prefix: 该模块所有路由的统一前缀
# tags: /docs 中的分组标题
router = APIRouter(prefix="/learn6", tags=["learn6"])


# ❌ 危险写法：密码直接泄漏给客户端
class UserIn1(BaseModel):
    username: str
    password: str
    email: EmailStr


@router.post("/create/user1")
async def create_user1(user: UserIn1):
    return user  # 响应里带着明文 password！


# response_model：出参的安全闸门
class UserIn2(BaseModel):
    """注册时客户端提交的模型"""

    username: str
    password: str
    email: EmailStr


class UserOut2(BaseModel):
    """返回给客户端的模型：绝对没有密码"""

    id: int
    username: str
    email: EmailStr


@router.post("/create/user2", response_model=UserOut2)
async def create_user2(user: UserIn2):
    return user


# 响应裁剪
# response_model_exclude_unset=True 只返回被显式赋过值的字段 回显"你刚改了什么"
# response_model_exclude_none=True 剔除 None 字段 瘦身列表响应
# response_model_exclude={"internal_note"} 按名字剔除 个别敏感字段
# response_model_include={...} 只保留指定字段 白名单输出
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


# 为 None 的字段直接不出现在响应里
@router.get("/items/{item_id}", response_model=Item, response_model_exclude_none=True)
async def read_item(item_id: int):
    return {"name": "键盘", "price": 399.0}
    # 响应: {"name": "键盘", "price": 399.0}  —— description/tax 被省略


# ------------------------ 自定义响应：文件、HTML、流式 --------------------
@router.get("/download/report")
async def download_report():
    return FileResponse(
        path="reports/1.pdf",
        filename="1.pdf",
        media_type="application/pdf",
    )


@router.get("/page", response_class=HTMLResponse)
def html_page():
    return "<h1>直接返回 HTML</h1>"


@router.get("/logs/stream")
def stream_logs():
    def log_generator():
        for i in range(100):
            yield f"日志行 {i}\n"

    # 流式响应：边生成边发送，适合大文件/实时日志
    return StreamingResponse(log_generator(), media_type="text/plain")
