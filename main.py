from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import crud, models, schemas, database
from database import engine, get_db
import os
from contextlib import asynccontextmanager

# Render部署生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建数据库表
    models.Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="校园轻社交+资源置换平台", 
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS中间件 - 生产环境中应限制为特定域名
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],  # 限制为前端域名，更安全
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "欢迎使用校园轻社交+资源置换平台API"}

# 用户相关路由
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@app.get("/users/")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# 资源置换相关路由
@app.post("/exchanges/", response_model=schemas.ExchangeResponse)
def create_exchange(exchange: schemas.ExchangeCreate, db: Session = Depends(get_db)):
    return crud.create_exchange(db=db, exchange=exchange)

@app.get("/exchanges/", response_model=list[schemas.ExchangeResponse])
def read_exchanges(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    exchanges = crud.get_exchanges(db, skip=skip, limit=limit)
    return exchanges

@app.get("/exchanges/{exchange_id}", response_model=schemas.ExchangeResponse)
def read_exchange(exchange_id: int, db: Session = Depends(get_db)):
    exchange = crud.get_exchange(db, exchange_id=exchange_id)
    if exchange is None:
        raise HTTPException(status_code=404, detail="交换信息不存在")
    return exchange

# 社交帖子相关路由
@app.post("/posts/", response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post)

@app.get("/posts/", response_model=list[schemas.PostResponse])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)