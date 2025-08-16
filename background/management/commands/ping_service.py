import requests
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Ping the service to keep it awake'

    def handle(self, *args, **kwargs):
        url = 'https://api.zilotech.org/health/'  # Use full URL on Render
        try:
            response = requests.get(url)
            self.stdout.write(self.style.SUCCESS(f'Pinged {url} - Status: {response.status_code}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to ping {url}: {e}'))
