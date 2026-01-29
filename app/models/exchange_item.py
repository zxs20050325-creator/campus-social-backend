from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class ExchangeItem(Base):
    __tablename__ = "exchange_items"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # 物品类别
    condition = Column(String(20), default="良好")  # 物品状况
    image_urls = Column(String(1000))  # 图片URL列表，用逗号分隔
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系定义
    owner = relationship("User", back_populates="exchanges")