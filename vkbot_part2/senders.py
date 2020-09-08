import vk_api
import requests
import random
from vk_api.longpoll import VkLongPoll, VkEventType


vk_session = vk_api.VkApi(token='9c2e8fb4b897d89744067019463ecc518810952aece084bdd390b13f13c6d9183c7c87e67613d18d54b95')
vk = vk_session.get_api()

def random_id ():
    rand = 0
    rand += random.randint(0, 10000000)
    return rand

def send_msg(id,text):
    vk.messages.send(user_id = id, message = text, keyboard = open("main_keyboard.json","r", encoding="UTF-8").read(), random_id = random_id ())

def send_reg_msg(id,text):
    vk.messages.send(user_id = id, message = text, keyboard = open("reg_keyboard.json","r", encoding="UTF-8").read(), random_id = random_id ())

def send_1msg(id,text):
    vk.messages.send(user_id = id, message = text, random_id = random_id ())

def send_stick(id, number):
    vk.messages.send(user_id = id, sticker_id = number, keyboard = open("main_keyboard.json","r", encoding="UTF-8").read(), random_id = random_id ())

