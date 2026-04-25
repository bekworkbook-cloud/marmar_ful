# src/shared/utils/datetime.py

from datetime import datetime, time


def today_start() -> datetime:
    now = datetime.now()
    return datetime.combine(now.date(), time.min)