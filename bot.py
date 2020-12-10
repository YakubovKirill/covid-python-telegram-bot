import config
import telebot
import COVID19Py
from telebot import types

TOKEN = config.TG_TOKEN

bot = telebot.TeleBot(TOKEN)
covid = COVID19Py.COVID19()
latest = covid.getLatest()

@bot.message_handler(commands = ['start'])
def first_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Во всём мире')
    btn2 = types.KeyboardButton('Украина')
    btn3 = types.KeyboardButton('Россия')
    btn4 = types.KeyboardButton('Беларусь')
    btn5 = types.KeyboardButton('США')
    btn6 = types.KeyboardButton('Польша')
    btn7 = types.KeyboardButton('Италия')
    btn8 = types.KeyboardButton('Литва')
    btn9 = types.KeyboardButton('Казахстан')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)

    infoMessage = f"<b>Привет {message.from_user.first_name} !</b>\n\nУкажи свою страну, чтобы узнать количество заболевших"
    bot.send_message(message.chat.id, infoMessage, parse_mode='html', reply_markup=markup)

@bot.message_handler(commands = ['help'])
def help_command(message):
    final_message = f"<u><b>Как пльзовться ботом</b></u>\n\nДля начала общения необходимо набрать команду /start\nЗаем нажать на кнопку необходимой страны\n\nВот и все :)\nЗдоровья тебе и соблюдай правила личной гигиены !)"
    bot.send_message(message.chat.id, final_message, parse_mode='html')

@bot.message_handler(content_types=['text'])
def send_text(message):
    country =  message.text.lower()
    final_message = ""
    if country == "сша":
        location = covid.getLocationByCountryCode("US")
    elif country == "россия":
        location = covid.getLocationByCountryCode("RU")
    elif country == "украина":
        location = covid.getLocationByCountryCode("UA")
    elif country == "беларусь":
        location = covid.getLocationByCountryCode("BY")
    elif country == "польша":
        location = covid.getLocationByCountryCode("PL")
    elif country == "италия":
        location = covid.getLocationByCountryCode("IT")
    elif country == "казахстан":
        location = covid.getLocationByCountryCode("KZ")
    elif country == "литва":
        location = covid.getLocationByCountryCode("LT")
    else:
        location = covid.getLatest()
        final_message = f"<u><b>Данные по всему миру:</b></u>\n\n<b>Заболевших: </b>{location['confirmed']:,}\n<b>Сметрей: </b>{location['deaths']:,}"
    
    if final_message == "":
        date = location[0]['last_updated'].split("T")
        time = date[1].split(".")
        final_message = f"<u><b>Данные по стране:</b></u>\n\nНаселение: {location[0]['country_population']:,}\nПоследнее обновление: {date[0]} {time[0]}\n\nПоследние данные:\n<b>Заболевших: </b>{location[0]['latest']['confirmed']:,}\n<b>Сметрей: </b>{location[0]['latest']['deaths']:,}"
        
    bot.send_message(message.chat.id, final_message, parse_mode='html')
    

bot.polling(none_stop=True)