from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.exchange_item import ExchangeItemCreate, ExchangeItemResponse, ExchangeItemUpdate
from app.services.exchange_service import (
    create_exchange_item as create_exchange_item_service,
    get_exchange_item as get_exchange_item_service,
    get_exchange_items as get_exchange_items_service,
    update_exchange_item as update_exchange_item_service,
    delete_exchange_item as delete_exchange_item_service
)
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=ExchangeItemResponse, status_code=status.HTTP_201_CREATED)
async def create_exchange_item(
    exchange_item: ExchangeItemCreate, 
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await create_exchange_item_service(db, exchange_item, current_user.id)


@router.get("/{exchange_item_id}", response_model=ExchangeItemResponse)
async def read_exchange_item(
    exchange_item_id: int, 
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    item = await get_exchange_item_service(db, exchange_item_id=exchange_item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="交换物品不存在"
        )
    return item


@router.get("/", response_model=List[ExchangeItemResponse])
async def read_exchange_items(
    skip: int = 0, 
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    items = await get_exchange_items_service(db, skip=skip, limit=limit)
    return items


@router.put("/{exchange_item_id}", response_model=ExchangeItemResponse)
async def update_exchange_item(
    exchange_item_id: int,
    exchange_item_update: ExchangeItemUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    item = await get_exchange_item_service(db, exchange_item_id=exchange_item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="交换物品不存在"
        )
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只能修改自己发布的物品"
        )
        
    updated_item = await update_exchange_item_service(db, exchange_item_id, exchange_item_update)
    if not updated_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="交换物品不存在"
        )
    return updated_item


@router.delete("/{exchange_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exchange_item(
    exchange_item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    item = await get_exchange_item_service(db, exchange_item_id=exchange_item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="交换物品不存在"
        )
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只能删除自己发布的物品"
        )
        
    success = await delete_exchange_item_service(db, exchange_item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="交换物品不存在"
        )
    return