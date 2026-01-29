from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, schemas
from datetime import datetime


# 用户相关CRUD操作
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = f"hashed_{user.password}"  # 实际项目中应该使用安全的哈希算法
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=fake_hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# 资源置换相关CRUD操作
def get_exchange(db: Session, exchange_id: int):
    return db.query(models.ExchangeItem).filter(models.ExchangeItem.id == exchange_id).first()


def get_exchanges(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ExchangeItem).offset(skip).limit(limit).all()


def create_exchange(db: Session, exchange: schemas.ExchangeCreate):
    db_exchange = models.ExchangeItem(
        title=exchange.title,
        description=exchange.description,
        category=exchange.category,
        condition=exchange.condition,
        image_urls=exchange.image_urls,
        is_available=exchange.is_available,
        owner_id=exchange.owner_id
    )
    db.add(db_exchange)
    db.commit()
    db.refresh(db_exchange)
    return db_exchange


def update_exchange(db: Session, exchange_id: int, exchange_update: schemas.ExchangeUpdate):
    db_exchange = get_exchange(db, exchange_id)
    if db_exchange:
        update_data = exchange_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_exchange, key, value)
        db.commit()
        db.refresh(db_exchange)
    return db_exchange


def delete_exchange(db: Session, exchange_id: int):
    db_exchange = get_exchange(db, exchange_id)
    if db_exchange:
        db.delete(db_exchange)
        db.commit()
    return db_exchange


# 社交帖子相关CRUD操作
def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()


def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(
        title=post.title,
        content=post.content,
        image_urls=post.image_urls,
        author_id=post.author_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post_id: int, post_update: schemas.PostUpdate):
    db_post = get_post(db, post_id)
    if db_post:
        update_data = post_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_post, key, value)
        db.commit()
        db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post