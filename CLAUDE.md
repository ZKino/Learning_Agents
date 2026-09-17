# CLAUDE.md

本文件为 Claude Code（claude.ai/code）在本仓库中处理代码时提供指导。

## 仓库概述

这是一个学习仓库（`Learning_Agents`），用于循序渐进地学习 FastAPI / Pydantic 的写法，内容按模块拆分为多个"学习单元"。项目使用 `uv` 管理依赖（`pyproject.toml` + `uv.lock`），以 `src` 式的包结构组织代码，但没有测试、linter 或 CI 配置。

## 项目结构

```
main.py          # 应用入口：创建 FastAPI 实例，统一挂载各路由（/api/v1 前缀）
api/v1/
  learn1.py      # 路径参数（Path 校验）
  learn2.py      # 查询参数（Query 校验、重复键 → list）
  learn3.py      # 请求体参数（Pydantic 模型、嵌套模型、Field 约束、HttpUrl）
  learn4.py      # 字段校验（field_validator / model_validator、EmailStr、response_model）
pyproject.toml   # uv 管理的项目元数据与依赖
uv.lock          # 锁定依赖版本
```

## 命令

所有命令在仓库根目录下运行。虚拟环境位于 `.venv`（Python 3.12.10，由 `uv` 创建）。

```bash
# 启动开发服务器（带自动重载）
.venv/Scripts/python -m uvicorn main:app --reload
# 或等价地：.venv/Scripts/uvicorn main:app --reload

# 交互式 API 文档（服务器运行时访问）
# http://127.0.0.1:8000/docs
```

本仓库没有测试套件、linter 或格式化工具的配置。

## 架构说明

- `main.py` 创建 `FastAPI` 实例（`app`，title="Learn FastAPI..."），并从 `api.v1` 导入各学习单元的路由，统一以 `prefix="/api/v1"` 挂载（`app.include_router(...)`）。新增学习单元时应同时在这里挂载。
- 每个 `learn*.py` 是独立的 FastAPI `APIRouter`，自带 `prefix="/learnN"` 与 `tags=["learnN"]`（用于 /docs 分组），因此完整路径形如 `/api/v1/learnN/...`。
- 现有路由一览：
  - `GET  /api/v1/learn1/items/{id}` — 路径参数，`Annotated[int, Path(ge=1, le=100)]`
  - `GET  /api/v1/learn2` — 查询参数，`page`/`size`/`keywords`/`tag`（重复键 `?tag=a&tag=b` 通过 `Annotated[list[str], Query()]` 捕获）
  - `POST /api/v1/learn3/create/goods` — 请求体，嵌套 Pydantic 模型（`Goods` 包含 `Image` 列表、`Seller`），URL 字段用 `HttpUrl`
  - `POST /api/v1/learn4/user/register` 与 `/user/register2` — `field_validator` 单字段校验 / `model_validator` 跨字段校验，`EmailStr` 邮箱校验，`response_model` 输出裁剪
- 全代码使用 Python 3.12 语法（`str | None`、`list[str]`），并使用 `Annotated[type, ...]` 元数据写法而非默认值参数写法。这是新增接口应遵循的约定。

## 开发约定

- 依赖由 `uv` 管理：`pyproject.toml` 中的 `dependencies` 是唯一依赖清单（当前：`fastapi[standard]`、`email-validator`）。新增依赖用 `uv add <pkg>`，不要手动改 `uv.lock`。
- 虚拟环境由 `uv` 创建于 `.venv`（Python 3.12），同步依赖用 `uv sync`。
- 新增学习单元时遵循既有模式：新建 `api/v1/learnN.py` 定义 `APIRouter`，然后在 `main.py` 中挂载。
- 根目录的 `.git` 跟踪整个 `Learning_Agents` 仓库。
