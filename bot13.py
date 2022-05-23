import telebot
from telebot import types # для указание типов
import sqlite3
import pytz
import datetime

day_time = datetime.datetime.now(pytz.timezone("Europe/Moscow"))

sessions = {}


#day2 = datetime.datetime.today() - datetime.timedelta(days=2)
#day1 = datetime.datetime.today() - datetime.timedelta(days=1)
#day0 = datetime.datetime.today() - datetime.timedelta(days=0)


connect = sqlite3.connect ("Zayavka.db", check_same_thread=False)
cursor = connect.cursor()
connect.execute("""CREATE TABLE IF NOT EXISTS Clock(
org TEXT,
name TEXT,
tech TEXT,
day TEXT,
joiningDate INTEGER
)
""") 
connect.commit()


bot = telebot.TeleBot('5256798982:AAHXhxQyopyvjF3PnQYSKmtTRiIElV3toYc')
@bot.message_handler(commands=['start'])
def startorg(message):
    user_id = message.chat.id
    sessions.update({ user_id: {'first_name': message.from_user.first_name} })
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Восток")
    btn2 = types.KeyboardButton("Строй инж-г")
    btn3 = types.KeyboardButton("Дорожники")
    btn4 = types.KeyboardButton("Газинвест")
    btn5 = types.KeyboardButton("АСВ")
    btn6 = types.KeyboardButton("ТНПС")
    btn7 = types.KeyboardButton("Тагазстрой")
    btn8 = types.KeyboardButton("База2")
    btn9 = types.KeyboardButton("Полистрой")
    btn10 = types.KeyboardButton("Другое")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10)
    org = [message.text]
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Выбери организацию".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def name(message):
    data = [message.chat.id]
    if(message.text == "Восток", "Строй инж-г", "Дорожники", "Газинвест", "АСВ", "ТНПС", "Тагазстрой", "База2", "Полистрой", "Другое"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Айнур")
        btn2 = types.KeyboardButton("Фаниль")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Выберите водителя", reply_markup=markup)
        bot.register_next_step_handler(message, tech) 

@bot.message_handler(content_types=['text'])
def tech(message):
    if(message.text in ['Айнур', 'Фаниль', 'Дорожники', 'Газинвест', 'АСВ', 'СПК', 'ТНПС', 'Тагазстрой', 'База2', 'Полистрой', 'Другое']):
        sessions[message.chat.id].update({'objectt': message.text})
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Щетка")
        btn2 = types.KeyboardButton("Кран25")
        btn3 = types.KeyboardButton("Кран32")
        btn4 = types.KeyboardButton("Cat/JCB")
        btn5 = types.KeyboardButton("КМУ")
        btn6 = types.KeyboardButton("Длинномер")
        btn7 = types.KeyboardButton("Самосвал")
        btn8 = types.KeyboardButton("Хундай 210")
        btn9 = types.KeyboardButton("Catгидро")
        btn10 = types.KeyboardButton("210гидро")
        btn11 = types.KeyboardButton("liuGong")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11)
        bot.send_message(message.chat.id, text="Выберите технику", reply_markup=markup)
        tech = [message.text] #нужно искать тут 
        bot.register_next_step_handler(message, day)

@bot.message_handler(content_types=['text'])
def day(message):
    day = [message.chat.id]
    if(message.text == "Щетка", "Кран25", "Кран32", "Cat/JCB", "КМУ", "Длинномер", "Самосвал", "Хундай 210", "Catгидро", "210гидро", "liuGong"):
        #sessions[message.chat.id].update({'data': datetime.datetime.today() - datetime.timedelta(days=1)})
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("День")
        btn2 = types.KeyboardButton("Ночь")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Выберите время суток", reply_markup=markup)
        bot.register_next_step_handler(message, save_link)

    #elif(message.text == "Сегодня"):
       # sessions[message.chat.id].update({'data': datetime.datetime.today() - datetime.timedelta(days=0)})
        #markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #btn1 = types.KeyboardButton("День")
       # btn2 = types.KeyboardButton("Ночь")
       # markup.add(btn1, btn2)
       # bot.send_message(message.chat.id, text="Выберите время суток", reply_markup=markup)
       # bot.register_next_step_handler(message, func2)



@bot.message_handler(content_types=['text'])  #реагирует на любые сообщения
def test(message):
    sessions[message.chat.id].update({'hour': message.text})
    

@bot.message_handler(content_types=['text'])          
def save_link(message):
    sessions[message.chat.id].update({'gas': message.text})
    input_data = sessions[message.chat.id]

    sessions[message.chat.id].update({'joiningDate': day_time})
    input_data = sessions[message.chat.id]
    print(input_data)
    cursor.execute("INSERT INTO Clock (org, name, tech, day, joiningDate) VALUES (?, ?, ?, ?, ?);", (message.chat.id, input_data['org'], input_data['name'], input_data['tech'], input_data['day'], input_data['joiningDate']))
    connect.commit()
    y_link = message.text
    bot.send_message(message.chat.id, "Сохранил!")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Новый день")
    markup.add(btn1)            
    bot.send_message(message.chat.id, text="{0.first_name}!".format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, start)
    




bot.polling(none_stop=True, interval=0)