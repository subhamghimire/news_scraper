from typing import Iterable

from app.core.base_scraper import BaseScraper
from app.core.rate_limiter import RateLimiter


class MyRepublicaScraper(BaseScraper):
    source_name = "MyRepublica"
    base_url = "https://myrepublica.nagariknetwork.com/"

    def __init__(self, rate_limiter: RateLimiter):
        super().__init__(rate_limiter)

    def fetch_listing(self) -> Iterable[str]:
        return []

    def fetch_article(self, url: str):
        raise NotImplementedError("MyRepublica scraper not yet implemented.")

