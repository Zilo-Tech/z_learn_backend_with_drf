from django.core.management.commands.runserver import Command as RunserverCommand
from background.scheduler import start_scheduler

class Command(RunserverCommand):
    def run(self, **options):
        print('Starting background scheduler...')
        start_scheduler()
        super().run(**options)
