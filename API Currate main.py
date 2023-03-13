import telebot
from APICurrateConf import keys, TOKEN
from APICurrateUtils import CryptoConverter, ConvertionException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'end'])
def money(message: telebot.types.Message):
    text = 'введите команду в формате: \n <валюта которую меняете> ' \
'<в какую валюту перевести>  <количество валюты>, чтобы увидеть список доступных валют : /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys:
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler()
def convert(message: telebot.types.Message):
    try:

        quote, base, amount, total_base = CryptoConverter.converter(message)
    except ConvertionException as e:
        bot.reply_to(message, f'ошибка пользователя\n {e}')

    except Exception as e:
        bot.reply_to(message, f'не удалось обработать команду\n {e}')
    else:
        text = f'цена {amount} {quote} в {base} - {float(total_base) * amount}'

        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)