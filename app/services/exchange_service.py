from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.exchange_item import ExchangeItem
from app.schemas.exchange_item import ExchangeItemCreate, ExchangeItemUpdate


async def create_exchange_item(db: AsyncSession, exchange_item: ExchangeItemCreate, owner_id: int):
    db_item = ExchangeItem(
        title=exchange_item.title,
        description=exchange_item.description,
        category=exchange_item.category,
        condition=exchange_item.condition,
        image_urls=exchange_item.image_urls,
        owner_id=owner_id
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def get_exchange_item(db: AsyncSession, exchange_item_id: int):
    stmt = select(ExchangeItem).where(ExchangeItem.id == exchange_item_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_exchange_items(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(ExchangeItem).offset(skip).limit(limit).order_by(ExchangeItem.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_exchange_item(db: AsyncSession, exchange_item_id: int, exchange_item_update: ExchangeItemUpdate):
    stmt = select(ExchangeItem).where(ExchangeItem.id == exchange_item_id)
    result = await db.execute(stmt)
    db_item = result.scalar_one_or_none()
    
    if db_item:
        for var, value in vars(exchange_item_update).items():
            if value is not None:
                setattr(db_item, var, value)
        await db.commit()
        await db.refresh(db_item)
        return db_item
    return None


async def delete_exchange_item(db: AsyncSession, exchange_item_id: int):
    stmt = select(ExchangeItem).where(ExchangeItem.id == exchange_item_id)
    result = await db.execute(stmt)
    db_item = result.scalar_one_or_none()
    
    if db_item:
        await db.delete(db_item)
        await db.commit()
        return True
    return False