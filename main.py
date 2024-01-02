from make_ribbon import make_ribbon_dict
from ribbon_RDB import ribbon_RDB
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
from collections import Counter
import operator


#######  make ribbon_RDB  #####
# make_ribbon_dict()



RIBBON = "6906121455:AAE1s-oUZZztlA1JOcgArWokcK84fcZBGUo"
JARVIS = "6357305111:AAHzb68csA1ojiDn620m7FFvDXcTP9tYu_s"

CURRENT_BOT = JARVIS
per_message = 1
bs_name = ""
# cwd = os.getcwd()
# print(cwd)


bot = telebot.TeleBot(CURRENT_BOT)

def add_preffix(bs_name):
    preffix = (4-len(bs_name))*"0"
    bs_name = "CR"+ preffix + bs_name
    if not bs_name in ribbon_RDB:
        bs_name = bs_name.replace("CR", "SE")
    return bs_name

def yandex_markup(bs_name,ribbon_RDB):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Yandex-навигатор", url=ribbon_RDB[bs_name]['yandex_map']))
    return markup
def make_output_sheet(message,bs_name,ribbon_RDB,markup):
    try:
        bot.send_message(message.chat.id, f"------ {bs_name} ------\n"
                                          f"Адрес: {ribbon_RDB[bs_name]['address']}\n"
                                          f"Координаты: {ribbon_RDB[bs_name]['coordinates']}\n"
                                          f"Конструктивный тип сайта: {ribbon_RDB[bs_name]['cunstruction']}\n"
                                          f"Ответственный: {ribbon_RDB[bs_name]['responcible']}\n",
                         reply_markup=yandex_markup(bs_name,ribbon_RDB))
    except Exception as ex:
        print(ex)


print("Бот Запущен")

###############  ОСНОВНОЙ КОД #################
@bot.message_handler()
def find_bs(message):
#####################################поиск по адресу ###################################
    global bs_name
    print('isalpha : ', "".join(message.text.split()).isalpha())
    if "".join(message.text.split()).isalpha():
        bs_name = message.text.upper()
        if len(bs_name.split()) > 1:
            keywords = []
            for keyword in bs_name.split():
                bs_string = ""
                for bs in ribbon_RDB:
                    if keyword in ribbon_RDB[bs]["address"].upper():
                        keywords.append(bs)
            counter =Counter(keywords)
            counter = dict(counter)
            # result = max(counter.iteritems(),key=operator.itemgetter(1))[0]
            # print(result)

            result = {element:count for element,count in counter.items() if count > 1}
            result_list = list(result)
            print(result_list)
            for bs in result_list:
                bs_string = f" {bs}\n{ribbon_RDB[bs]['address']}\n\n" + bs_string

            if len(bs_string) > 4095:
                for x in range(0, len(bs_string), 4095):
                    bot.send_message(message.chat.id, text=bs_string[x:x + 4095])
            else:
                bot.send_message(message.chat.id, text=bs_string)
        else:
            bs_string = ""
            for bs in ribbon_RDB:
                if bs_name in ribbon_RDB[bs]["address"].upper():
                    bs_string = f" {bs}\n{ribbon_RDB[bs]['address']}\n\n" + bs_string

            if len(bs_string) > 4095:
                for x in range(0, len(bs_string), 4095):
                    bot.send_message(message.chat.id, text=bs_string[x:x + 4095])
            else:
                bot.send_message(message.chat.id, text=bs_string)


    elif len(message.text.split()) > 1:
        bs_name = message.text.upper()
        for bs in bs_name.split():
            bs_name = bs
            if bs_name in ribbon_RDB:
                make_output_sheet(message, bs_name, ribbon_RDB, markup=yandex_markup(bs_name, ribbon_RDB))
            else:
                bs_name = add_preffix(bs_name)
                make_output_sheet(message, bs_name, ribbon_RDB, markup=yandex_markup(bs_name, ribbon_RDB))

    elif len(message.text.split()) == 1:
        bs_name = message.text.upper()
        if bs_name in ribbon_RDB:
            make_output_sheet(message, bs_name, ribbon_RDB, markup=yandex_markup(bs_name, ribbon_RDB))
        else:
            bs_name = add_preffix(bs_name)
            make_output_sheet(message, bs_name, ribbon_RDB, markup=yandex_markup(bs_name, ribbon_RDB))


try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
    # bot.polling(none_stop=True)
except Exception as ex:
    print(ex)
    time.sleep(15)