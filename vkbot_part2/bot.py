import vk_api
import requests
from senders import send_msg, send_stick, send_reg_msg, send_1msg
import sql_command as sql
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session =vk_api.VkApi(token='9c2e8fb4b897d89744067019463ecc518810952aece084bdd390b13f13c6d9183c7c87e67613d18d54b95')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

def indentefi(id):
    user_get = vk.users.get(user_ids = id)[0]
    name = user_get["first_name"]
    last_name = user_get["last_name"]
    sql.insert(id,name+" "+last_name,"none","none")
    return name

def indentefi_2(id):
    user_get = vk.users.get(user_ids = id)[0]
    name = user_get["first_name"]
    return name

def set_group(id):
    if sql.none_group(id):
        send_reg_msg(id,"Ваш блок уже указан.")
    else:
        send_reg_msg(id, "Введите номер блока:")
        for block in longpoll.listen():
            if block.type == VkEventType.MESSAGE_NEW and block.to_me and block.text:
                if block.user_id == id: 
                    try:
                        number = int(block.text)
                    except ValueError:
                        send_reg_msg(id,"Введите число (3 или 4)")
                    else:
                        if number == 3 or number == 4:
                            sql.set_group(id, block.text)
                            send_reg_msg(id,"Отлично.")
                            break
                        send_reg_msg(id,"Введите число (3 или 4)")
                else:
                    send_1msg(block.user_id,"В данный момент, не могу ответить. Напишите позже")

def set_room(id):
    if sql.none_room(id):
        send_reg_msg(id,"Ваша комната уже указана.")
    else:
        send_reg_msg(id, "Введите номер комнаты:")
        for block in longpoll.listen():
            if block.type == VkEventType.MESSAGE_NEW and block.to_me and block.text:
                if block.user_id == id: 
                    try:
                        number = int(block.text)
                    except ValueError:
                        send_reg_msg(id,"Введите число (от 1 до 6)")
                    else:
                        if number > 0 and number < 7:
                            sql.set_room(id, block.text)
                            send_reg_msg(id,"Отлично.")
                            break
                        send_reg_msg(id,"Введите число (от 1 до 6)")
                else:
                    send_1msg(block.user_id,"В данный момент, не могу ответить. Напишите позже")

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        id = event.user_id
        msg = event.text.lower()
        if sql.select_user(id):
            if msg == "start" or msg == "hi" or msg == "привет" or msg == "hello" or msg == "ало":
                send_msg(id, "Приветствую " + indentefi_2(id) + "\nНаша группа помогает в организации дежурств на кухне для 3 и 4 блока. Дежурный будет проинформирован заранее. Если есть вопросы по поводу организации группы, пишите админам группы.")
            elif msg == "номер блока":
                set_group(id)
            elif msg == "регистрация":
                send_reg_msg(id,"Производится регистрация пользователя " + indentefi_2(id))
            elif msg == "номер комнаты":
                set_room(id)
            elif msg == "кто сегодня дежурит?":
                send_msg(id,"Дай подумать.")
            elif msg == "проверка данных / выход":
                send_msg(id,"Если данные указаны с ошибкой, писать администраторам группы.")
                data = sql.select_all_from_users(id)
                if data[0][2] == 'none' and data[0][3] == 'none':
                    send_msg(id,"Ваши данные:\nИмя: " + data[0][1] + "\nБлок: неизвестно" + "\nНомер комнаты: неизвестно" )
                elif data[0][2] == 'none':
                    send_msg(id,"Ваши данные:\nИмя: " + data[0][1] + "\nБлок: неизвестно" + "\nНомер комнаты: " + data[0][3])
                elif data[0][3] == 'none':
                    send_msg(id,"Ваши данные:\nИмя: " + data[0][1] + "\nБлок: " + data[0][2] + "\nНомер комнаты: неизвестно")
                else:
                    send_msg(id,"Ваши данные:\nИмя: " + data[0][1] + "\nБлок: " + data[0][2] + "\nНомер комнаты: " + data[0][3])
            else:
                send_1msg(id,"Неизвестная команда!")
        else:
            name = indentefi(id)
            send_msg(id,"Приветствую " + name)