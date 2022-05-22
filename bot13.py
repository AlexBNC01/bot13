import telebot
from telebot import types # для указание типов
import sqlite3

import datetime
day_time = datetime.datetime.now(pytz.timezone("Europe/Moscow"))

sessions = {}


#day2 = datetime.datetime.today() - datetime.timedelta(days=2)
#day1 = datetime.datetime.today() - datetime.timedelta(days=1)
#day0 = datetime.datetime.today() - datetime.timedelta(days=0)


connect = sqlite3.connect ("Zayavka.db", check_same_thread=False)
cursor = connect.cursor()
connect.execute("""CREATE TABLE IF NOT EXISTS Clock(
id INTEGER,
first_name TEXT,
data TEXT,
day TEXT,
objectt TEXT,
tech TEXT,
hour INTEGER,
gas INTEGER, 
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
    markup.add(btn1)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я посчитаю Часы работы. Просто  пройди опрос после рабочего дня!".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def org(message):
    data = [message.chat.id]
    if(message.text == "Начать"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Вчера")
        btn2 = types.KeyboardButton("Сегодня")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Выберите день за который заполняете часы", reply_markup=markup)
        bot.register_next_step_handler(message, func) 

@bot.message_handler(content_types=['text'])
def func(message):
    day = [message.chat.id]
    if(message.text == "Вчера"):
        sessions[message.chat.id].update({'data': datetime.datetime.today() - datetime.timedelta(days=1)})
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("День")
        btn2 = types.KeyboardButton("Ночь")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Выберите время суток", reply_markup=markup)
        bot.register_next_step_handler(message, func2)

    elif(message.text == "Сегодня"):
        sessions[message.chat.id].update({'data': datetime.datetime.today() - datetime.timedelta(days=0)})
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("День")
        btn2 = types.KeyboardButton("Ночь")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Выберите время суток", reply_markup=markup)
        bot.register_next_step_handler(message, func2)

@bot.message_handler(content_types=['text'])
def func2(message):    
    if(message.text == "День", "Ночь"):
        sessions[message.chat.id].update({'day': message.text})
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
        bot.send_message(message.chat.id, text="Выберите Объект", reply_markup=markup)
        bot.register_next_step_handler(message, han) 

@bot.message_handler(content_types=['text'])
def han(message):

    if(message.text in ['Восток', 'Строй инж-г', 'Дорожники', 'Газинвест', 'АСВ', 'СПК', 'ТНПС', 'Тагазстрой', 'База2', 'Полистрой', 'Другое']):
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
        bot.register_next_step_handler(message, han1)

@bot.message_handler(content_types=['text'])
def han1(message):

    if(message.text in ["Щетка", "Кран25", "Кран32", "Cat/JCB", "КМУ", "Длинномер", "Самосвал", "Хундай 210", "Catгидро", "210гидро", "liuGong"]):
        sessions[message.chat.id].update({'tech': message.text})
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        btn1 = types.KeyboardButton("1")
        btn2 = types.KeyboardButton("2")
        btn3 = types.KeyboardButton("3")
        btn4 = types.KeyboardButton("4")
        btn5 = types.KeyboardButton("5")
        btn6 = types.KeyboardButton("6")
        btn7 = types.KeyboardButton("7")
        btn8 = types.KeyboardButton("8")
        btn9 = types.KeyboardButton("9")
        btn10 = types.KeyboardButton("10")
        btn11 = types.KeyboardButton("11")
        btn12 = types.KeyboardButton("12")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12)
        bot.send_message(message.chat.id, text="Выберите часы, или напишите с помощью клавиатуры, если в путевке +30 минут", reply_markup=markup)
        bot.register_next_step_handler(message, test)
        hour = [message.text] #нужно искать тут 


@bot.message_handler(content_types=['text'])  #реагирует на любые сообщения
def test(message):
    sessions[message.chat.id].update({'hour': message.text})
    gas = [message.text] #нужно искать тут 
    
    if (message.text in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '4,5', '5,5', '6,5', '7,5', '8,5', '9,5', '10,5', '11,5', '12,5', '4.3', '5.3', '6.3', '7.3', '8.3', '9.3', '10.3', '11.3', '12.3', '4.5', '5.5', '6.5', '7.5', '8.5', '9.5', '10.5', '11.5', '12.5', '4,3', '5,3', '6,3', '7,3', '8,3', '9,3', '10,3', '11,3', '12,3']):    #Если содержимое == 'One',то 
          bot.reply_to(message, 'Сколько сегодня заправились? (в литрах)')   #Bot reply 'Введите текст'
          @bot.message_handler(content_types=['text'])  #Создаём новую функцию ,реагирующую на любое сообщение
          def message_input_step(message):
               global text  #объявляем глобальную переменную
               text = message.text
               bot.reply_to(message, f'Ваш текст: {message.text}')
          bot.register_next_step_handler(message, save_link) #добавляем следующий шаг, перенаправляющий пользователя на message_input_step
# Убрать клаву

@bot.message_handler(content_types=['text'])          
def save_link(message):
    sessions[message.chat.id].update({'gas': message.text})
    input_data = sessions[message.chat.id]

    sessions[message.chat.id].update({'joiningDate': day_time})
    input_data = sessions[message.chat.id]
    print(input_data)
    cursor.execute("INSERT INTO Clock (id, first_name, data, day, objectt, tech, hour, gas, joiningDate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", (message.chat.id, input_data['first_name'], input_data['data'], input_data['day'], input_data['objectt'], input_data['tech'], input_data['hour'], input_data['gas'], input_data['joiningDate']))
    connect.commit()
    y_link = message.text
    bot.send_message(message.chat.id, "Сохранил!")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Новый день")
    markup.add(btn1)            
    bot.send_message(message.chat.id, text="{0.first_name}! Нажми кнопку завтра, после рабочего дня!".format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, start)
    




bot.polling(none_stop=True, interval=0)