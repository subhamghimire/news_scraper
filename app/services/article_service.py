import logging
from typing import Dict, Optional

from sqlalchemy.orm import Session

from app.models.news_article import NewsArticle


logger = logging.getLogger(__name__)


class ArticleService:
    def __init__(self, session: Session):
        self.session = session

    def save_article(self, source_id: int, article: Dict) -> Optional[NewsArticle]:
        url = article.get("article_url")
        if not url:
            logger.warning("Skipping article without URL for source_id=%s", source_id)
            return None

        existing = self.session.query(NewsArticle).filter_by(article_url=url).first()
        if existing:
            return None

        record = NewsArticle(
            source_id=source_id,
            title=article.get("title", ""),
            content=article.get("content"),
            image_url=article.get("image_url"),
            article_url=url,
            author=article.get("author"),
            language=article.get("language", "en"),
            published_at=article.get("published_at"),
            published_date_raw=article.get("published_date_raw"),
        )
        self.session.add(record)
        self.session.commit()
        logger.info("Saved article for source_id=%s url=%s", source_id, url)
        return record

