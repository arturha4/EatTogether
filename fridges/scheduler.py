from apscheduler.schedulers.background import BackgroundScheduler
from tasks import check_expired_products


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_expired_products, 'interval', minutes=60)
    scheduler.start()
