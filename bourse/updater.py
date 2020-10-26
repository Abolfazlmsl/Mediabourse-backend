from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .feed import update_timeframe_candles, test


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_timeframe_candles, 'interval', hours=1, start_date='2020-10-25 22:30:00')
    # scheduler.add_job(test, 'cron', hour=16, minute=30)
    scheduler.start()