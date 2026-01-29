from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.post import Post, Comment
from app.schemas.post import PostCreate, PostUpdate, CommentCreate
from typing import Optional


async def create_post(db: AsyncSession, post: PostCreate, author_id: int):
    db_post = Post(
        title=post.title,
        content=post.content,
        author_id=author_id,
        image_urls=post.image_urls
    )
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


async def get_post(db: AsyncSession, post_id: int):
    stmt = select(Post).where(Post.id == post_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(Post).offset(skip).limit(limit).order_by(Post.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_post(db: AsyncSession, post_id: int, post_update: PostUpdate):
    stmt = select(Post).where(Post.id == post_id)
    result = await db.execute(stmt)
    db_post = result.scalar_one_or_none()
    
    if db_post:
        for var, value in vars(post_update).items():
            if value is not None:
                setattr(db_post, var, value)
        await db.commit()
        await db.refresh(db_post)
        return db_post
    return None


async def delete_post(db: AsyncSession, post_id: int):
    stmt = select(Post).where(Post.id == post_id)
    result = await db.execute(stmt)
    db_post = result.scalar_one_or_none()
    
    if db_post:
        await db.delete(db_post)
        await db.commit()
        return True
    return False


async def create_comment(db: AsyncSession, comment: CommentCreate, author_id: int):
    db_comment = Comment(
        content=comment.content,
        post_id=comment.post_id,
        author_id=author_id
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def get_comments(db: AsyncSession, post_id: int):
    stmt = select(Comment).where(Comment.post_id == post_id).order_by(Comment.created_at.asc())
    result = await db.execute(stmt)
    return result.scalars().all()