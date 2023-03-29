import requests


def get_course():
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
