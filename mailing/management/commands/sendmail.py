from django.core.management import BaseCommand
from mailing.services import check_adn_run_mailings


class Command(BaseCommand):

    def handle(self, *args, **options):
        check_adn_run_mailings()

