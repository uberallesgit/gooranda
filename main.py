from RDB import RDB
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
from collections import Counter
import operator

GOORANDA = "6001130506:AAFNMXUh-iE3zdSq7PK2cpWWg4JFg_swwwg"
JARVIS = "6357305111:AAHzb68csA1ojiDn620m7FFvDXcTP9tYu_s"

CURRENT_BOT = JARVIS
per_message = 1
bs_name = ""
# cwd = os.getcwd()
# print(cwd)


bot = telebot.TeleBot(CURRENT_BOT)

def add_preffix(bs_name):
    preffix = (4-len(bs_name))*"0"
    bs_name = "CR" + preffix + bs_name
    if not bs_name in RDB:
        bs_name = bs_name.replace("CR", "SE")
    return bs_name

def yandex_markup(bs_name,RDB):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Yandex-навигатор", url=RDB[bs_name]['yandex_map']))
    return markup

def find_responcible(RDB,bs_name):
    responcible = ""
    Djankoysky = ["джанкойский", "джанкой","первомайский","первомайское", "красноперекопский", "армянcкий", "нижнегорский"]
    Yevpatoriysky = ["евпатория,","евпатория","сакский","саки","черноморский","раздольненский"]
    Simferopolsky = ["симферополь","симферопольский","красногвардейский","белогорский","бахчисарайский", "ялта", "ялтинский","алушта"]
    Feodosiysky = ["феодосия","судак","ленинский","керчь","кировский","советский"]
    address = RDB[bs_name]["address"]

    for part in address.replace("."," ").replace(","," ").replace("-"," ").split():
        print(bs_name[:2])
        if bs_name[:2] == "SE":

            responcible = "Гречишников Анатолий"
            break
        elif part.lower() in Djankoysky:
            responcible = "Пономаренко Алексей"
            break
        elif part.lower() in Yevpatoriysky:
            responcible = "Пономаренко Алексей"
            break
        elif part.lower() in Simferopolsky:
            responcible = "Буханов Дмитрий"
            break
        elif part.lower() in Feodosiysky:
            responcible = "Грачёв Алексей"
            break

    return responcible

def make_output_sheet(message,bs_name,RDB,markup):
    try:
        bot.send_message(message.chat.id, f"------ {bs_name} ------\n"
                                          f"КТК формат:  {RDB[bs_name]['arc_id']}\n"
                                          f"Адрес: {RDB[bs_name]['address']}\n"
                                          f"Координаты: {RDB[bs_name]['coordinates']}\n"
                                          f"Конструктивный тип сайта: {RDB[bs_name]['constructional_type']}\n"
                                          f"Ответственный: {find_responcible(RDB,bs_name)}\n",
                         reply_markup=yandex_markup(bs_name,RDB))
    except Exception as ex:
        print(ex)

def make_output_arc_sheet(message,bs_name,RDB,markup):
    try:
        bot.send_message(message.chat.id, f"------ {bs_name} ------\n"
                                          f"КТК формат:  {RDB[bs_name]['arc_id']}\n"
                                          f"Адрес: {RDB[bs_name]['address']}\n"
                                          f"Координаты: {RDB[bs_name]['coordinates']}\n"
                                          f"Конструктивный тип сайта: {RDB[bs_name]['constructional_type']}\n"
                                          f"Ответственный: {find_responcible(RDB,bs_name)}\n",
                         reply_markup=yandex_markup(bs_name,RDB))
    except Exception as ex:
        print(ex)

print("Бот Запущен")

###############  ОСНОВНОЙ КОД #################
@bot.message_handler()
def find_bs(message):
#####################################поиск по адресу ###################################
    global bs_name
    if (message.text[:3]).upper() == "ARC":
        for bs_name in RDB:
            ktk_bs_name = message.text.upper()
            ktk_cell = RDB[bs_name]["arc_id"]
            if ktk_cell != None:
                print(ktk_cell)
                if ktk_bs_name[3:] in ktk_cell:
                    make_output_arc_sheet(message, bs_name, RDB, markup=yandex_markup(bs_name, RDB))

    elif "".join(message.text.split()).isalpha():
        bs_name = message.text.upper()
        if len(bs_name.split()) > 1:
            keywords = []
            for keyword in bs_name.split():
                bs_string = ""
                for bs in RDB:
                    if keyword in RDB[bs]["address"].upper():
                        keywords.append(bs)
            counter =Counter(keywords)
            counter = dict(counter)
            result = {element: count for element, count in counter.items() if count > 1}
            result_list = list(result)
            print(result_list)
            for bs in result_list:
                bs_string = f" {bs}\n{RDB[bs]['address']}\n\n" + bs_string

            if len(bs_string) > 4095:
                for x in range(0, len(bs_string), 4095):
                    bot.send_message(message.chat.id, text=bs_string[x:x + 4095])
            else:
                bot.send_message(message.chat.id, text=bs_string)
        else:
            bs_string = ""
            for bs in RDB:
                if bs_name in RDB[bs]["address"].upper():
                    bs_string = f" {bs}\n{RDB[bs]['address']}\n\n" + bs_string

            if len(bs_string) > 4095:
                for x in range(0, len(bs_string), 4095):
                    bot.send_message(message.chat.id, text=bs_string[x:x + 4095])
            else:
                bot.send_message(message.chat.id, text=bs_string)


    elif len(message.text.split()) > 1:
        bs_name = message.text.upper()
        for bs in bs_name.split():
            bs_name = bs
            if bs_name in RDB:
                make_output_sheet(message, bs_name, RDB, markup=yandex_markup(bs_name, RDB))
            else:
                bs_name = add_preffix(bs_name)
                make_output_sheet(message, bs_name, RDB, markup=yandex_markup(bs_name, RDB))

    elif len(message.text.split()) == 1:
        bs_name = message.text.upper()
        if bs_name in RDB:
            make_output_sheet(message, bs_name, RDB, markup=yandex_markup(bs_name, RDB))
        else:
            bs_name = add_preffix(bs_name)
            make_output_sheet(message, bs_name, RDB, markup=yandex_markup(bs_name, RDB))


try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
    # bot.polling(none_stop=True)
except Exception as ex:
    print(ex)
    time.sleep(15)