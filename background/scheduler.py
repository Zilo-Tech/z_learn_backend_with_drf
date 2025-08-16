from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import subprocess

def start_scheduler():
    print("🔄 Starting APScheduler...")
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        lambda: subprocess.run(['python', 'manage.py', 'ping_service']),
        trigger=IntervalTrigger(minutes=5),
        name='Keep service awake',
        replace_existing=True
    )
    scheduler.start()
