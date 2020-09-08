import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
import sqlite3


vk_session = vk_api.VkApi(token='9c2e8fb4b897d89744067019463ecc518810952aece084bdd390b13f13c6d9183c7c87e67613d18d54b95')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
url='photo233651797_457240325'
upload = VkUpload(vk_session)
connect = sqlite3.connect("DataBase.db")
cursor = connect.cursor()

def sender(id, text):
    vk.messages.send(user_id=id, message=text, keyboard = open("keyboard.json", "r", encoding="UTF-8").read(), random_id = 0)

def send_stick(id,stick_number):
    vk.messages.send(user_id = id, sticker_id = stick_number, keyboard = open("keyboard.json","r", encoding="UTF-8").read(), random_id =0)

def insert(id,name,group,room):
        cmd = "INSERT INTO users VALUES (%d,'%s','%s','%s')" % (id,name,group,room)
        cursor.execute(cmd)
        connect.commit()
def select(id):
    cmd = "SELECT * FROM users WHERE user_id = %d" % id
    cursor.execute(cmd)
    result = cursor.fetchone()
    if result is None:
        return False
    return True

def select_name(id):
    cmd = "SELECT name FROM users WHERE user_id = %d" % id
    cursor.execute(cmd)
    result = cursor.fetchone()
    return result

def registration(id):
    sender(id,"Ок, сейчас будем вносить вас в список дежурств.\n Будьте добры вводить коректную информацию(Если хотите выйти из режима регистрации, введите команду \" выход\").")
    k = 0
    sender(id,"Введите свое имя (Фамилия И.О):")
    for reg_event in longpoll.listen():
        if reg_event.type == VkEventType.MESSAGE_NEW and reg_event.to_me and reg_event.text:
            msg = reg_event.text.lower()
            if msg == "выход":
                sender(id,"Вы вышли с режима регистрации!")
                k = 4
            elif k == 0:
                name = msg
                k = k+1
                sender(id,"Введите номер блока(3/4):")
            elif k == 1:
                group = msg
                k = k +1
                sender(id,"Введите номер комнаты:")
            elif k == 2:
                room = msg
                sender(id,"Проверьте валидность данных(да - если все верно, нет - если есть ошибки):\n Для упрощения работы, все данные записываются прописными буквами.")
                sender(id,"Имя: " + name)
                sender(id,"блок: " + group)
                sender(id,"комната: " + room)
                k = k+1
            elif k == 3 and msg == "да":
                sender(id,"Отлично, больше ничего не требуется.")
                insert(id,name,group,room)
                k = k+1
                
            elif k == 3 and msg == "нет":
                sender(id,"Тогда введите все данные заново. Сначало ваше имя(Фамилия И.О):")
                k = 0
        elif k == 4:
            break


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        msg = event.text.lower()
        id = event.user_id
        if msg == 'привет' or msg == 'start' or msg == 'старт' or msg == 'здарова' or msg == 'здрасти' or msg == 'hello' or msg == 'hi' or msg == 'ало' or msg == 'alo':
            if select(id):
                name =  select_name(id)[0]
                sender(id,"Здравствуйте "+ name.upper())
            else:
                send_stick(id,11758)
        elif msg == 'регистрация':
            if select(id):
                sender(id,"Вы уже зарегистрированы в системе. \n В случае ошибки, писать администраторам группы!")
            else:
                registration(id)
        elif msg == "кто сегодня дежурит?":
            sender(id,"Я пока что не на столько умный, приходите завтра!")
        elif msg == "пока" or msg == 'чао' or msg == 'bye' or msg == 'до завтра' or msg == 'пока пока' or msg == 'до встречи':
            send_stick(id,16369)
        else:
            sender(id,'МОЯ ТВОЯ НЕ  ПОНИМАТЬЪ')
