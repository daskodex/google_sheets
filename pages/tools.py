import requests
from .models import ParseResult
import matplotlib.pyplot as plt
import telegram
from decouple import config

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

    parseresult = ParseResult.objects.all()
    x = []
    y = []

    for result in parseresult:
        x.append(result.delivery_time)
        y.append(result.price)

    plt.plot(x, y)
    plt.xlabel('Дата заказах')
    plt.ylabel('Стоимость заказ в $')
    plt.title('Данные о заказа по датам')
    plt.savefig('.\core\static\core\graph.png')




def SendTGMessage(msg):
    """
    Надо указать token бота и chat_id (можно получить через (@getmyid_bot)
    """
    bot = telegram.Bot(token=config('TG_TOKEN'))
    bot.sendMessage(chat_id=config('TG_CHAT_ID'), text=msg)