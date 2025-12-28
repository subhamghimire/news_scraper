import logging
from typing import Dict, Generator, Iterable
from urllib.parse import urlparse

from app.core.rate_limiter import RateLimiter


logger = logging.getLogger(__name__)


class BaseScraper:
    source_name: str = ""
    base_url: str = ""

    def __init__(self, rate_limiter: RateLimiter):
        self.rate_limiter = rate_limiter

    def fetch_listing(self) -> Iterable[str]:
        raise NotImplementedError

    def fetch_article(self, url: str) -> Dict:
        raise NotImplementedError

    def run(self) -> Generator[Dict, None, None]:
        try:
            urls = list(self.fetch_listing())
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Scraper %s listing fetch failed: %s", self.source_name, exc, exc_info=True)
            return

        for url in urls:
            try:
                domain = urlparse(url).netloc
                self.rate_limiter.wait(domain)
                yield self.fetch_article(url)
            except Exception as exc:  # pragma: no cover - defensive
                logger.warning("Scraper %s failed for %s: %s", self.source_name, url, exc, exc_info=True)

