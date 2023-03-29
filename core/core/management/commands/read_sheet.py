from django.core.management.base import BaseCommand
from pprint import pprint
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from pages.models import ParseResult
from pages.tools import get_course


class Command(BaseCommand):
    help = 'Google Sheets Reader'

    def handle(self, *args, **options):
        CREDENTIALS_FILE = 'credentials.json'
        spreadsheet_id = '1pw4NmxdZtjlsQGk24rO00UEap57EwN_d3MGJs3wnWQs'

        # Авторизуемся и получаем service — экземпляр доступа к API
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

        # Пример чтения файла
        values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range='A1:D60',
            majorDimension='COLUMNS'
        ).execute()

        course = get_course()

        ParseResult.objects.all().delete()

        for i in range(1,len(values['values'][0])-1):
            price_rur = float(float(values['values'][2][i]) * float(course)),
            print(values['values'][0][i],
                  values['values'][1][i],
                  price_rur,
                  values['values'][3][i])
            ParseResult(number=values['values'][0][i],
                        order_id=values['values'][1][i],
                        price=price_rur,
                        delivery_time=values['values'][3][i]).save()