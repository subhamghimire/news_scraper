from typing import Iterable

from app.core.base_scraper import BaseScraper
from app.core.rate_limiter import RateLimiter


class HimalayanTimesScraper(BaseScraper):
    source_name = "HimalayanTimes"
    base_url = "https://thehimalayantimes.com/"

    def __init__(self, rate_limiter: RateLimiter):
        super().__init__(rate_limiter)

    def fetch_listing(self) -> Iterable[str]:
        return []

    def fetch_article(self, url: str):
        raise NotImplementedError("HimalayanTimes scraper not yet implemented.")

