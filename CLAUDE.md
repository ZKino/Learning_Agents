# CLAUDE.md

本文件为 Claude Code（claude.ai/code）在本仓库中处理代码时提供指导。

## 仓库概述

这是一个学习仓库（`Learning_Agents`），用于学习如何使用 Python 构建 Agent/工具。目前包含一个位于 `fastapi_01/` 下的 FastAPI 学习项目。代码库刻意保持精简——一个单文件的 FastAPI 应用，没有打包、测试或 CI 配置。

## 项目：fastapi_01

一个教程风格的 FastAPI 应用，用于演示参数处理的各种写法。所有内容都在 `fastapi_01/main.py` 中——没有包结构或多模块布局。

### 命令

所有命令都在 `fastapi_01/` 目录下运行。虚拟环境已创建在 `fastapi_01/.venv`（Python 3.12.10，依赖：FastAPI、uvicorn、pydantic、python-multipart）。

```bash
cd fastapi_01

# 启动开发服务器（带自动重载）
.venv/Scripts/python -m uvicorn main:app --reload
# 或者等价地：.venv/Scripts/uvicorn main:app --reload

# 交互式 API 文档（服务器运行时访问）
# http://127.0.0.1:8000/docs
```

本仓库没有测试套件、linter 或格式化工具的配置。

### 架构说明

- `main.py` 创建了一个 `FastAPI` 实例（`app`），并通过装饰器注册路由。该应用也可以被编程方式导入和检查，例如 `main.app.routes`。
- 路由使用现代的 `Annotated[type, ...]` 元数据写法，而不是传统的默认值参数写法。这是新增接口应遵循的约定：
  - 路径参数：`Annotated[int, Path(title=..., ge=1, le=100)]`
  - 查询参数：`Annotated[int | None, Query(min_length=1, max_length=50)]`
  - 重复的查询键（例如 `?tag=a&tag=b`）通过 `Annotated[list[str] | None, Query()]` 捕获。
- 请求体使用 Pydantic v2 的 `BaseModel` 子类配合 `Field(...)` 约束来建模，包括嵌套模型（例如 `Goods` 包含 `Image` 列表和一个 `Seller`）。URL 类型的字段使用 `HttpUrl`。
- 全代码使用 Python 3.12 语法（`str | None`、`list[str]`）。

### 开发约定

- 添加新依赖时，将其安装到现有的 venv 中（`.venv/Scripts/pip install <pkg>`），而不是新建环境。目前没有 `requirements.txt`——如果依赖增多，可能需要引入一个。
- 根目录的 `.git` 跟踪整个 `Learning_Agents` 仓库；目前 `fastapi_01/` 是唯一未被跟踪的内容，`main` 分支上还没有任何提交。
