from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Refreshes clips and feeds'

    def handle(self, *args, **options):
        self.stdout.write("Refreshing clips")
        call_command('refresh_clips')
        self.stdout.write("Refreshing feeds")
        call_command('refresh_feeds')
