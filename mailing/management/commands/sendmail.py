from django.core.management import BaseCommand
from mailing.mailing_functions import check_adn_run_mailings


class Command(BaseCommand):

    def handle(self, *args, **options):
        check_adn_run_mailings()

