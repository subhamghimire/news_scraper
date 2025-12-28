from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.news_source import NewsSource


class NewsArticle(Base):
    __tablename__ = "news_articles"
    __table_args__ = (UniqueConstraint("article_url", name="uq_article_url"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    article_url = Column(String(500), nullable=False)
    author = Column(String(255), nullable=True)
    source_id = Column(Integer, ForeignKey("news_sources.id"), nullable=False)
    language = Column(Enum("ne", "en", name="article_language_enum"), nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    published_date_raw = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    source = relationship(NewsSource, lazy="joined")

