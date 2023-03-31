from django.core.management.base import BaseCommand

from pages.tools import DrowGraph, SendTGMessage, ReadSheets


class Command(BaseCommand):
    help = 'Google Sheets Reader'

    def handle(self, *args, **options):
        expired_log = ReadSheets()
        DrowGraph()
        SendTGMessage(expired_log)

