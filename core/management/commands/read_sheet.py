from django.core.management.base import BaseCommand
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from pages.models import ParseResult
from pages.tools import get_course, DrowGraph, SendTGMessage
from datetime import datetime, date
from decouple import config

class Command(BaseCommand):
    help = 'Google Sheets Reader'

    def handle(self, *args, **options):

        CREDENTIALS_FILE = config('CREDENTIALS_FILE')
        SPREADSHEETS_ID = config('SPREADSHEETS_ID')

        # Авторизуемся и получаем service — экземпляр доступа к API
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

        # Пример чтения файла
        values = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEETS_ID,
            range='A1:D60',
            majorDimension='COLUMNS'
        ).execute()

        #TODO поменять на динамическое определение диапазона

        ParseResult.objects.all().delete()

        expired_log = ''

        for i in range(1, len(values['values'][0])):

            parsed_price = int(float(values['values'][2][i]) * float(get_course()))

            d = datetime.strptime(values['values'][3][i], "%d.%m.%Y")
            parsed_date = d.strftime('%Y-%m-%d')

            expired = True if str(date.today()) > parsed_date else False

            #Функция шлет сообщения от бота о том что заказ просрочен

            ParseResult(number=values['values'][0][i],
                        order_id=values['values'][1][i],
                        price=parsed_price,
                        delivery_time=parsed_date,
                        delivery_time_orig=values['values'][3][i],
                        expired=expired,
                        ).save()

            if expired:
                expired_log += f'Заказ с ID:{values["values"][1][i]} просрочен\n'

        DrowGraph()

        SendTGMessage(expired_log)

