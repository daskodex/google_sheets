from django.core.management.base import BaseCommand

from pages.tools import DrowGraph, SendTGMessage, ReadSheets


class Command(BaseCommand):
    help = 'Google Sheets Reader'

    def handle(self, *args, **options):

        # функция читает гугл-таблицу
        expired_log = ReadSheets()

        # функция рисует график стоимость \ дата
        DrowGraph()

        # функция шлет сообщения от бота о том что заказ просрочен
        SendTGMessage(expired_log)

