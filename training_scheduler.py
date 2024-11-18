import asyncio
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A_B_test_project.settings')
os.environ.setdefault('TF_ENABLE_ONEDNN_OPTS', '0')
django.setup()

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from A_B_test.recs_manager import RecsManager
import A_B_test.test_config as config

# Recommendations and test management
config.recs_manager = RecsManager(config_path=config.config_path)


class TrainingScheduler:
    """
    Custom class to schedule models training
    """

    def __init__(self):
        self.scheduler = AsyncIOScheduler()

        # Training models every day at 00:00
        self.scheduler.add_job(
            config.recs_manager.update_recs,
            'cron',
            hour=00, minute=00,
            id='train_models',
            replace_existing=True
        )

    def run_scheduler(self):
        print("Starting scheduler...")
        self.scheduler.start()

        try:
            print("Scheduler is running")
            asyncio.get_event_loop().run_forever()
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()
            print("Scheduler ended")


if __name__ == '__main__':
    scheduler = TrainingScheduler()
    scheduler.run_scheduler()
