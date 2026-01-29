# 校园轻社交+资源置换平台后端

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # 应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth_middleware.py
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── exchange_item.py
│   ├── schemas/             # Pydantic模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── exchange_item.py
│   ├── api/                 # API路由
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   ├── posts.py
│   │   │   └── exchanges.py
│   │   └── deps.py          # 依赖注入
│   └── services/            # 业务逻辑
│       ├── __init__.py
│       ├── user_service.py
│       ├── post_service.py
│       └── exchange_service.py
├── migrations/              # 数据库迁移
├── tests/                   # 测试文件
├── scripts/                 # 脚本文件
├── .env.example             # 环境变量示例
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
└── pyproject.toml           # 项目配置
```

## 功能特点

- 用户注册和登录（JWT认证）
- 发布和浏览社交动态（帖子）
- 发布和浏览可置换的物品
- 关注其他用户
- 评论和点赞功能

## 技术栈

- Python 3.11
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL (数据库)
- Redis (缓存)
- Docker (容器化)

## 安装与运行

1. 克隆项目
2. 安装依赖：`pip install -e .`
3. 设置环境变量（参考 .env.example）
4. 运行应用：`python -m app.main`

## API 文档

启动应用后，在 `/api/v1/docs` 路径下可以访问 Swagger UI 文档。