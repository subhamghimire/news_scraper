from typing import Dict, Iterable, List
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.core.base_scraper import BaseScraper
from app.core.http_client import fetch_html
from app.core.rate_limiter import RateLimiter
from app.services.date_parser import parse_date


class KantipurScraper(BaseScraper):
    source_name = "Kantipur"
    base_url = "https://ekantipur.com/"
    listing_url = urljoin(base_url, "news")

    def __init__(self, rate_limiter: RateLimiter):
        super().__init__(rate_limiter)

    def fetch_listing(self) -> Iterable[str]:
        html = fetch_html(self.listing_url)
        soup = BeautifulSoup(html, "html.parser")
        links: List[str] = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/"):
                href = urljoin(self.base_url, href)
            if href.startswith(self.base_url) and "/news/" in href and href not in links:
                links.append(href)
            if len(links) >= 20:
                break
        return links

    def fetch_article(self, url: str) -> Dict:
        html = fetch_html(url)
        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else ""
        image_tag = soup.find("img")
        image_url = image_tag["src"] if image_tag and image_tag.has_attr("src") else None
        paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
        content = "\n".join(paragraphs)

        time_tag = soup.find("time")
        published_raw = time_tag.get_text(strip=True) if time_tag else ""
        published_at, published_date_raw = parse_date(published_raw, language_hint="ne")

        return {
            "title": title,
            "content": content,
            "image_url": image_url,
            "article_url": url,
            "author": None,
            "language": "ne",
            "published_at": published_at,
            "published_date_raw": published_date_raw,
        }

