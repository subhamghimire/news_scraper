from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from app.config import settings


def start_scheduler(run_all_scrapers) -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        run_all_scrapers,
        "interval",
        minutes=settings.scrape_interval_minutes,
        next_run_time=datetime.now(),
        coalesce=True,
        max_instances=1,
        misfire_grace_time=60,
    )
    scheduler.start()
    return scheduler

