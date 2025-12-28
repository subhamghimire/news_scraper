from typing import Optional

import backoff
import httpx

from app.config import settings


def _build_client() -> httpx.Client:
    return httpx.Client(
        timeout=settings.request_timeout_seconds,
        headers={"User-Agent": settings.user_agent},
        follow_redirects=True,
    )


@backoff.on_exception(backoff.expo, (httpx.HTTPError,), max_tries=3)
def fetch(url: str) -> httpx.Response:
    with _build_client() as client:
        return client.get(url)


def fetch_html(url: str, encoding: Optional[str] = None) -> str:
    response = fetch(url)
    if encoding:
        response.encoding = encoding
    response.raise_for_status()
    return response.text

