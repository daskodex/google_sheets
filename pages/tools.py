import requests
from .models import ParseResult
import matplotlib.pyplot as plt
import telegram
from decouple import config
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from pages.models import ParseResult
from datetime import datetime, date
import time


def time_of_function(function):
    def wrapped(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        print(time.time() - start_time)
        return result

    return wrapped


def get_course():
    # функция получения текущего курса доллара США к рублю.
    try:
        data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        convert_rate = data['Valute']['USD']['Value']

    except:
        convert_rate = -1

    return convert_rate

    # print(data['Valute']['USD'])
    # {'CharCode': 'USD',
    #  'ID': 'R01235',
    #  'Name': 'Доллар США',
    #  'Nominal': 1,
    #  'NumCode': '840',
    #  'Previous': 74.1373,
    #  'Value': 74.1567}


def DrowGraph():
    # функция постоения графика
    # TODO 1.В задании нет, но лучше упорядочить даты и убрать дубли
    # TODO 2.Повернуть подписи по оси Y
    # TODO 3.Замасштабоировать график
    # TODO 4.Переместить файл графика в static/img на продакте

    parseresult = ParseResult.objects.order_by('-delivery_time')
    x = []
    y = []

    for result in parseresult:
        x.append(result.delivery_time)
        y.append(result.price_usd)

    plt.plot(x, y)
    plt.xlabel('Дата заказах')
    plt.ylabel('Стоимость заказ в $')
    plt.title('Данные о заказа по датам')
    plt.xticks(rotation=90)
    plt.savefig('.\core\static\core\graph.png')


def SendTGMessage(msg):
    """
    Функция отправки сообщая в телеграмм пользователя от имени бота
    Надо указать token бота и chat_id (можно получить через (@getmyid_bot)
    """
    if not msg:
        return False

    try:
        bot = telegram.Bot(token=config('TG_TOKEN'))
        bot.sendMessage(chat_id=config('TG_CHAT_ID'), text=msg)
        return True
    except telegram.error.Unauthorized:
        print('Ошибка: telegram.error.Unauthorized: Unauthorized, проверьте токен бота')
        return False

    except telegram.error.BadRequest:
        print('Ошибка: telegram.error.BadRequest:, проверьте ID чата в телеграм')
        return False


@time_of_function
def ReadSheets():
    CREDENTIALS_FILE = config('CREDENTIALS_FILE')
    SPREADSHEETS_ID = config('SPREADSHEETS_ID')

    # Авторизуемся и получаем service — экземпляр доступа к API
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    # Чтение таблицы, скорость работы не зависит от длинны диапазона, ставим 99999 строк

    values = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEETS_ID,
        range='A1:D99999',
        majorDimension='COLUMNS'
    ).execute()

    ParseResult.objects.all().delete()

    expired_log = ''

    for i in range(1, len(values['values'][0])):

        price_rur = int(float(values['values'][2][i]) * float(get_course()))

        d = datetime.strptime(values['values'][3][i], "%d.%m.%Y")
        parsed_date = d.strftime('%Y-%m-%d')

        expired = True if str(date.today()) > parsed_date else False

        # Функция шлет сообщения от бота о том что заказ просрочен

        ParseResult(number=values['values'][0][i],
                    order_id=values['values'][1][i],
                    price_usd=values['values'][2][i],
                    price_rur=price_rur,
                    delivery_time=parsed_date,
                    delivery_time_orig=values['values'][3][i],
                    expired=expired,
                    ).save()

        if expired:
            expired_log += f'Заказ с №:{values["values"][1][i]} просрочен\n'

    return expired_log
