from pyrogram import Client
import json
from datetime import datetime
import time
import os
import shutil

api_id = 15911419
api_hash = "f1e47a3de0595d329d9b143168612595"
menu = ''

def cls():
    os.system('cls')

def exists(var):
    var_exists = var in locals() or var in globals()
    return var_exists

def check_chat(chat_name):

        # Открываем файл со строками
        try:
            with open("check_chan.txt", "r", encoding="UTF-8") as f:
                suc_chats = f.read()
        # Если его нет, то создаем переменную.
        except:
            suc_chats = []

        # Проверка совпадений строк
        x = 0
        for chat in suc_chats:
            if (chat == chat_name):
                x = 1

        # Сценарий найденого совпадения.
        if x == 1:
            ok = 1

        else:
            chat_name = '@' + chat_name + '\n'
            with open('store/check_chan.txt', "a", encoding="UTF-8") as f:
                f.write(chat_name)


# Добавление ботов.
def menu_1():
    while True:
        cls()
        num_file = 0
        Name_for_folder = 'bot'
        phone_number = input("[Введите \"0\" чтобы выйти.]\nВведите номер вашего аккаунта(+79997775533): ").strip()

        if(phone_number == '0'):
            return 0

        # Открываем файл со строками
        try:
            with open("bots.json", "r", encoding="UTF-8") as f:
                bots = json.loads(f.read())

        # Если его нет, то создаем переменную.
        except:
            bots = []

        # Проверка совпадений строк
        x = 0
        for bot in bots:
            if (phone_number == bot['number']):
                x = 1

        # Сценарий найденого совпадения.
        if x == 1:
            input('Этот аккаунт уже есть в бд. Нажмите Enter и введите иной номер.')

        # Сценарий нового аккаунта
        else:
            # Создание сессии.
            with Client(":memory:", api_id, api_hash, phone_number=phone_number) as app:
                # Создаем JSON формат бота
                session_bot = app.export_session_string()
                bots.append({
                    'number': phone_number,
                    'session': session_bot,
                    'time': 0,
                    'chats': 'None'
                })
                with open("bots.json", "w", encoding="UTF-8") as f:
                    f.write(json.dumps(bots, indent=4))
            input('Бот успешно добавлен! Нажмите Enter и введите следующий номер.')

# Запуск спама.
def menu_2():
    cls()
    while True:

        # Читаем бд ботов
        with open("bots.json", "r", encoding="UTF-8") as f:
            bots = json.loads(f.read())

        # Открываем текст.
        with open('channel.txt', "r", encoding="UTF-8") as f:
            channel = f.read()

        for bot in bots:
            if bot['time'] < time.time():
                for chat in bot['chats']:
                    # Проверяем, требуется ли действие от бота.
                    z = 0
                    if chat['ready'] < time.time():
                        z = 1

                # Если требуется, то:
                if z == 1:
                    z = 0
                    try:
                        with Client(bot['session'], api_id, api_hash) as app:
                            for chat in bot['chats']:
                                # Проверяем подписку на чат.
                                if chat['podpis'] == 'True':
                                    if(chat['ready'] < time.time()):
                                        try:
                                            # Отправка сообщения
                                            mess_id = app.get_history(channel, limit=1)
                                            app.forward_messages(chat['name'], channel, mess_id[0]['message_id'])
                                            # app.send_video(chat['name'], 'video.mp4', caption=text)
                                            #app.send_photo(chat['name'], photo, caption=text)
                                            chat['ready'] = time.time() + 7200
                                            bot['time'] = time.time() + 120
                                            print('[' + bot['number'] + "] Сообщение отправлено.[" + chat['name'] + ']')
                                            check_chat(chat['name'])
                                            break
                                        except:
                                            # Не удалось отправить сообщение.
                                            print('[' + bot['number'] + "] Ошибка. Не удалось отправить сообщение. [" + chat['name'] + ']')
                                    else:
                                        # Не прошел интервал сообщений
                                        print('[' + bot['number'] + "] Чат не требует отправки.[" + chat['name'] + ']')
                    except: print('[' + bot['number'] + "] Не удалось авторизоваться.")
                else: print('[' + bot['number'] + "] Бот готов, но от него не требуется действий.")
            else: print('[' + bot['number'] + "] Бот спит.")

        with open("bots.json", "w", encoding="UTF-8") as f:
            f.write(json.dumps(bots, indent=4))

        # Считаем статистику
        fal = 0
        tru = 0
        for bot in bots:
            for chat in bot['chats']:
                fal += 1
                if chat['ready'] > time.time():
                    tru += 1

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        stat_mes = '[' + str(current_time) + '][MCK]Круг окончен спим 2 минуты. [' + str(tru) + '/' + str(fal) +']' + '\n'
        with open('stat_mes.txt', "a", encoding="UTF-8") as f:
            f.write(stat_mes)

        print('')
        print(stat_mes)
        print('')
        time.sleep(120)

# Добавление чатов в бд.
def menu_3():
    cls()
    i = 0 # Счетчик

    # Открываем файл с новыми чатами.
    try:
        with open('Store/new_chan.txt', "r", encoding="UTF-8") as f:
            text = f.readlines()
    except:
        input('Нет файла new_chan.txt')
        return 0

    for ln in text:

        # Открываем бд чатов. Если пусто то создаем переменную.
        try:
            with open("chats.json", "r", encoding="UTF-8") as f:
                    chats = json.loads(f.read())
        except:
            chats = []

        i += 1
        # Форматирование чатов
        if ln[0] == '@':
            ln = ln[1:]
            ln = ln[:-1]

        else:
            print('['+ str(i) +']Внимание! Ошибка формата!')
            continue

        # Проверка дубликатов.
        z = 0
        for chat in chats:
            if (chat['name'] == ln):
                z = 1
        if(z == 1):
            print('[' + str(i) + ']Внимение! Дубликат!')
        else:
            # Создание нового чата в формате JSON
            print('[' + str(i) + ']Добавлен!')
            chats.append({
                "name": ln
            })
            with open("chats.json", "w", encoding="UTF-8") as f:
                f.write(json.dumps(chats, indent=4))
    input('\nОперация завершена.')

# Перераспределение чатов.
def menu_4():
    cls()
    # Открываем бд чатов. Если пусто то ошибка.
    try:
        with open("chats.json", "r", encoding="UTF-8") as f:
            chats = json.loads(f.read())
    except:
        input('Нет файла chats.json')
        return 0

    # Создаем список чатов.
    ch_names = []
    for chat in chats:
        ch_names.append(chat['name'])

    # Открываем бд ботов. Если пусто то ошибка.
    try:
        with open("bots.json", "r", encoding="UTF-8") as f:
            bots = json.loads(f.read())
    except:
        input('Нет файла bots.json')
        return 0

    # Промежуточная статистика
    num_bots = len(bots) - 1
    num_chats = len(ch_names)
    num_chats_on_bot = num_chats // num_bots
    input("Количество чатов: " + str(num_chats) + ". Количество ботов: " + str(num_bots) + ". Количество чатов на 1 бота: " + str(num_chats_on_bot) + ".")

    # Читаем бд ботов
    with open("bots.json", "r", encoding="UTF-8") as f:
        bots = json.loads(f.read())

    # Создаем списки каждому боту.
    i = 0
    z = 0
    ch_bot = []

    for ln in ch_names:

        i += 1
        ln = {
        "name": ln,
        "interval": 120,
        "podpis": "False",
        "ready": 0
        }
        ch_bot.append(ln)

        if(i == num_chats_on_bot):
            bots[z]['chats'] = ch_bot
            with open('bots.json', "w", encoding="UTF-8") as f:
                f.write(json.dumps(bots, indent=4))
            print(z)
            i = 0
            z += 1
            ch_bot = []
    print(z)
    z = z - 1
    bots[z]['chats'] = ch_bot
    with open('bots.json', "w", encoding="UTF-8") as f:
        f.write(json.dumps(bots, indent=4))
    input("Конец операции.")

def menu_5():

    # Читаем ботов
    with open("bots.json", "r", encoding="UTF-8") as f:
        bots = json.loads(f.read())

    i = 0
    for bot in bots:
        with Client(bot['session'], api_id, api_hash) as app:
            chats = app.get_dialogs()
            for dialog in chats:
                try:
                    i += 1
                    app.leave_chat(dialog.chat.id, delete=True)
                    print('[' + str(i) + '][' + bot['number'] + '] Отписался от чата.')
                except:
                    print('Не удалось отписаться от чата.')

def menu_6():
    while True:
        # Читаем ботов
        with open("bots.json", "r", encoding="UTF-8") as f:
            bots = json.loads(f.read())

        for bot in bots:
            if bot['time'] < time.time():
                for chat in bot['chats']:
                    if chat['podpis'] == "False":
                        # Подписываемся
                        try:
                            with Client(bot['session'], api_id, api_hash) as app:
                                app.join_chat(chat['name'])
                                chat['podpis'] = "True"
                                bot['time'] = time.time() + 420
                                with open("bots.json", "w", encoding="UTF-8") as f:
                                    f.write(json.dumps(bots, indent=4))
                                print('[' + bot['number'] + "] Подписался на чат. [" + chat['name'] + ']')
                                break

                        except:
                            # Не удалось подписаться на чат.
                            print('[' + bot['number'] + "] Не удалось подписаться на чат. [" + chat['name'] + ']')

            else: print('[' + bot['number'] + "] Бот спит.")
        fal = 0
        tru = 0
        for bot in bots:
            for chat in bot['chats']:
                if chat['podpis'] == 'True':
                    tru += 1
                fal += 1

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        stat = '[' + str(current_time) + '][MCK]Круг окончен спим 5 минут. [' + str(tru) + '/' + str(fal) +']' + '\n'
        with open('stat.txt', "a", encoding="UTF-8") as f:
            f.write(stat)

        print('')
        print(stat)
        print('')
        time.sleep(300)

while True:
    cls()
    menu = input('1.Запустить спам.\n2.Добавить бота.\n3.Добавить чаты в бд.\n4.Распределить чаты.\n5.Отписаться от всех чатов.\n6.Запустить подписку на чаты.\n0.Выход.\n\nВвод: ')

    if menu == '1':
        menu_2()

    if menu == '2':
        menu_1()

    if menu == '3':
        menu_3()

    if menu == '4':
        menu_4()

    if menu == '5':
        menu_5()

    if menu == '6':
        menu_6()

    if menu == '0':
        exit()
