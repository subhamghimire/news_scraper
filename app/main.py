import logging
import time
from typing import List

from app.config import settings
from app.core.rate_limiter import RateLimiter
from app.models.base import Base, engine, get_session
from app.models.news_source import NewsSource
from app.scheduler import start_scheduler
from app.services.article_service import ArticleService
from app.sites.kantipur import KantipurScraper
from app.sites.onlinekhabar import OnlineKhabarScraper
from app.sites.setopati import SetopatiScraper


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

SEED_SOURCES: List[dict] = [
    {"name": "Kantipur", "base_url": "https://ekantipur.com/", "language": "ne", "is_active": True},
    {"name": "OnlineKhabar", "base_url": "https://www.onlinekhabar.com/", "language": "ne", "is_active": True},
    {"name": "Setopati", "base_url": "https://www.setopati.com/", "language": "ne", "is_active": True},
    {"name": "HimalayanTimes", "base_url": "https://thehimalayantimes.com/", "language": "en", "is_active": False},
    {"name": "MyRepublica", "base_url": "https://myrepublica.nagariknetwork.com/", "language": "en", "is_active": False},
    {"name": "KathmanduPost", "base_url": "https://kathmandupost.com/", "language": "en", "is_active": False},
    {"name": "Ratopati", "base_url": "https://ratopati.com/", "language": "ne", "is_active": False},
    {"name": "NepalNews", "base_url": "https://nepalnews.com/", "language": "en", "is_active": False},
    {"name": "Gorkhapatra", "base_url": "https://gorkhapatraonline.com/", "language": "ne", "is_active": False},
    {"name": "Bizmandu", "base_url": "https://bizmandu.com/", "language": "ne", "is_active": False},
]


def seed_sources() -> None:
    with get_session() as session:
        for source in SEED_SOURCES:
            exists = session.query(NewsSource).filter_by(name=source["name"]).first()
            if not exists:
                session.add(NewsSource(**source))
        session.commit()


def run_all_scrapers() -> None:
    rate_limiter = RateLimiter(settings.rate_limit_delay_seconds)
    scrapers = [KantipurScraper(rate_limiter), OnlineKhabarScraper(rate_limiter), SetopatiScraper(rate_limiter)]

    with get_session() as session:
        article_service = ArticleService(session)
        for scraper in scrapers:
            source = session.query(NewsSource).filter_by(name=scraper.source_name, is_active=True).first()
            if not source:
                continue

            count = 0
            for article in scraper.run():
                if count >= settings.max_articles_per_run:
                    break
                article_service.save_article(source.id, article)
                count += 1


def main() -> None:
    seed_sources()
    scheduler = start_scheduler(run_all_scrapers)
    logger.info("Scheduler started with interval %s minutes", settings.scrape_interval_minutes)
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        scheduler.shutdown()
        logger.info("Scheduler stopped.")


if __name__ == "__main__":
    main()

