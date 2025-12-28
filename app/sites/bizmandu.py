from typing import Iterable

from app.core.base_scraper import BaseScraper
from app.core.rate_limiter import RateLimiter


class BizmanduScraper(BaseScraper):
    source_name = "Bizmandu"
    base_url = "https://bizmandu.com/"

    def __init__(self, rate_limiter: RateLimiter):
        super().__init__(rate_limiter)

    def fetch_listing(self) -> Iterable[str]:
        return []

    def fetch_article(self, url: str):
        raise NotImplementedError("Bizmandu scraper not yet implemented.")

