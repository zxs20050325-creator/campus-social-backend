from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import hash_password
from typing import Optional


async def create_user(db: AsyncSession, user: UserCreate):
    hashed_pwd = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pwd,
        full_name=user.full_name,
        bio=user.bio
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, user_id: int = None, email: str = None):
    stmt = select(User)
    if user_id:
        stmt = stmt.where(User.id == user_id)
    elif email:
        stmt = stmt.where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(User).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_user(db: AsyncSession, user_id: int, user_update):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()
    
    if db_user:
        for var, value in vars(user_update).items():
            if value is not None:
                setattr(db_user, var, value)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    return None


async def delete_user(db: AsyncSession, user_id: int):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()
    
    if db_user:
        await db.delete(db_user)
        await db.commit()
        return True
    return False