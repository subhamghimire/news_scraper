# News Scraper

Python scraper for Nepal news sites with MySQL storage, language/date handling, and 5-minute scheduling via APScheduler.

## Features
- Scrapes multiple Nepal news sites (Kantipur, OnlineKhabar, Setopati implemented; others stubbed).
- Nepali/English language detection and Nepali date parsing.
- Rate limiting per domain, retrying HTTP client.
- MySQL persistence with dedup on `article_url`.
- Interval scheduler (runs immediately on start, then every 5 minutes by default).

## Requirements
- Python 3.10+ (tested on 3.13)
- MySQL instance reachable from the app

## Setup
```bash
cd ~/scrap/nepal_news_scraper
python -m venv ../venv
source ../venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## Configuration
Create `.env` in project root (copy from `.env.example`):
```
DATABASE_URL=mysql+pymysql://USER:PASS@HOST:3306/DBNAME
SCRAPE_INTERVAL_MINUTES=5
REQUEST_TIMEOUT_SECONDS=10
USER_AGENT="NepalNewsBot/1.0"
RATE_LIMIT_DELAY_SECONDS=2
MAX_ARTICLES_PER_RUN=50
```

## Database schema (MySQL)
```sql
CREATE TABLE IF NOT EXISTS news_sources (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  base_url VARCHAR(255) NOT NULL,
  language ENUM('ne','en','both') NOT NULL DEFAULT 'both',
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS news_articles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(500) NOT NULL,
  content TEXT,
  image_url VARCHAR(500),
  article_url VARCHAR(500) NOT NULL,
  author VARCHAR(255),
  source_id INT NOT NULL,
  language ENUM('ne','en') NOT NULL,
  published_at DATETIME NULL,
  published_date_raw VARCHAR(255),
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_article_url (article_url),
  KEY idx_source_published (source_id, published_at),
  CONSTRAINT fk_news_articles_source
    FOREIGN KEY (source_id) REFERENCES news_sources(id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## Running
From project root:
```bash
python -m app.main
```
- Seeds `news_sources` if missing.
- Runs all active scrapers immediately, then every `SCRAPE_INTERVAL_MINUTES`.
- Logs to stdout.

## Notes
- Deduplication via `article_url` unique index and pre-insert check.
- If you interrupt with Ctrl+C mid-run, uncommitted inserts in that session roll back.
- To temporarily disable a site, set `is_active=0` in `news_sources`.

