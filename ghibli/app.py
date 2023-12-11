from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler

class AppNameConfig(AppConfig):
    name = 'ghibli'
    def ready(self):
        from movies.utils import scheduler
        scheduler()
