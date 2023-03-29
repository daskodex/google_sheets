from django.core.management.base import BaseCommand
from pprint import pprint
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials




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
            range='A1:D50',
            majorDimension='COLUMNS'
        ).execute()
        # pprint(values['values'])

        for row in values['values']:
            pprint(row[0])
