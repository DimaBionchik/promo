import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InputMediaPhoto
import gspread

gc = gspread.service_account(filename="my-test-project-408312-296aa9c49a83.json")
sh_connection = gc.open_by_url('https://docs.google.com/spreadsheets/d/17SIijNnjvkGk1-gxV5sBIdxZA3lHdNfWHqi-cQNFw-Q')
worksheet1 = sh_connection.sheet1
list_of_lists = worksheet1.get_all_values()
state = 0
temp2 = None
#print(list_of_lists)


bot = telebot.TeleBot('6365084070:AAHMTRnWKoEzlWTRjINPgFUdWugmZ98IMe0')


markets ={}
markets_info = {}
promo_info ={}
user_states = {}

for j in list_of_lists[1:]:
    if j[8] not in markets.keys():
        markets[j[8]] = [j[0]]
    else:
        if j[0] not in markets[j[8]]:
            markets[j[8]].append(j[0])

for j in list_of_lists[1:]:
    if j[0] not in promo_info.keys():
        promo_info[j[0]] = [j[3]]
    else:
        if j[3] not in promo_info[j[0]]:
            promo_info[j[0]].append(j[3])

for i in list_of_lists[1:]:
    key = i[0]
    value = {i[3]: i[4:8]}

    if key not in markets_info:
        markets_info[key] = value
    else:
        markets_info[key].update(value)




@bot.message_handler(commands=['start'])
def handle_start(message):
    global state
    if state == 0:
        markupI = InlineKeyboardMarkup()
        for name in markets:
            markupI.add(InlineKeyboardButton(name, callback_data=name))
        bot.send_message(message.chat.id, "Выберите категорию магазинов  в которой хотите получить скидку ⬇️",
                         reply_markup=markupI)
        state = state + 1



@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global state, temp2
    if state == 1:
        for category in markets.keys():
            if call.data == category:
                markupI = InlineKeyboardMarkup()
                for item in markets.get(category, []):
                    markupI.add(InlineKeyboardButton(item, callback_data=item))
                try:
                    if call.message:
                         bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=markupI)
                         state = state+1
                except Exception as e:
                    print(f"Error editing message reply markup: {e}")



    elif state == 2:
        for k213 in promo_info.keys():
            if call.data == k213:
                temp2 = k213
                markupI = InlineKeyboardMarkup()
                for item_info in promo_info.get(k213, []):
                    markupI.add(InlineKeyboardButton(item_info, callback_data=item_info))
                bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=markupI)
                state = state + 1

    elif state == 3:
        if call.data == '/start':
            state = 0
            temp2 = None
            handle_start(call.message)
        else:
            bot.send_message(call.message.chat.id,
                             'Чтобы воспользоваться акцией необходимо: перейти по ссылке или скопировать промокод и ввести его на сайте или приложении магазина')
            bot.send_message(call.message.chat.id, "\n".join(markets_info[temp2][call.data]))
            markupI = InlineKeyboardMarkup()


            markupI.add(InlineKeyboardButton('В меню', callback_data='/start'))
            bot.send_message(call.message.chat.id, 'Куда отправимся за скидками дальше?', reply_markup=markupI)


print("r")
bot.infinity_polling()