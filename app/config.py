import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "")
    scrape_interval_minutes: int = int(os.getenv("SCRAPE_INTERVAL_MINUTES", "5"))
    request_timeout_seconds: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))
    user_agent: str = os.getenv("USER_AGENT", "NepalNewsBot/1.0")
    rate_limit_delay_seconds: float = float(os.getenv("RATE_LIMIT_DELAY_SECONDS", "2"))
    max_articles_per_run: int = int(os.getenv("MAX_ARTICLES_PER_RUN", "50"))


settings = Settings()

