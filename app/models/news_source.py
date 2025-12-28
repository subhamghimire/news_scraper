from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, func

from app.models.base import Base


class NewsSource(Base):
    __tablename__ = "news_sources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    base_url = Column(String(255), nullable=False)
    language = Column(Enum("ne", "en", "both", name="language_enum"), nullable=False, default="both")
    is_active = Column(Boolean, nullable=False, server_default="1")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

