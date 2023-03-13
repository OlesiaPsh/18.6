import json
import requests
from APICurrateConf import keys, APIKey

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def converter(message):
        values = message.text.split()
        if len(values) != 3:
            raise ConvertionException('некорректное количество параметров')
        quote, base, amount = values
        if quote == base:
            raise ConvertionException(f'невозможно конвертировать одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        #r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        r = requests.get(f'https://currate.ru/api/?get=rates&pairs={quote_ticker}{base_ticker}&key={APIKey}')
        total_base = json.loads(r.content)['data'][f'{quote_ticker}{base_ticker}']

        return quote, base, amount, total_base