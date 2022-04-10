import os
import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload


class User:
    def __init__(self):
        self.liked_memes = set()
        self.disliked_memes = set()


class Quizier:
    def __init__(self):
        self.answ_first_q = set()
        self.answ_second_q = set()
        self.answ_third_q = set()
        self.answ_fourth_q = set()
        self.answ_fifth_q = set()
        self.answ_sixth_q = set()
        self.answ_seventh_q = set()
        self.answ_eigth_q = set()

    def ask_question(self, recipient_id):
        if recipient_id not in self.answ_first_q:
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("Красный", color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button("Зелёный", color=VkKeyboardColor.POSITIVE)
            keyboard.add_button("Синий", color=VkKeyboardColor.PRIMARY)
            send_msg_with_keyboard("Какой цвет вам нравится больше всего?", recipient_id, keyboard)
            self.answ_first_q.add(recipient_id)
            return
        if recipient_id not in self.answ_second_q:
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("A", color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()
            keyboard.add_button("B", color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button("C", color=VkKeyboardColor.PRIMARY)
            send_msg_with_keyboard("Какая буква вам нравится больше всего?", recipient_id, keyboard)
            self.answ_second_q.add(recipient_id)
            return
        if recipient_id not in self.answ_third_q:
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("1", color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button("2", color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button("3", color=VkKeyboardColor.PRIMARY)
            keyboard.add_button("4", color=VkKeyboardColor.SECONDARY)
            send_msg_with_keyboard("Какая цифра нравится вам больше всего?", recipient_id, keyboard)
            self.answ_third_q.add(recipient_id)
            return
        if recipient_id not in self.answ_fourth_q:
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("&#128014;", color=VkKeyboardColor.POSITIVE)
            keyboard.add_button("&#128015;	", color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button("&#128046;", color=VkKeyboardColor.POSITIVE)
            keyboard.add_button("&#128040;", color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button("&#128005;", color=VkKeyboardColor.POSITIVE)
            keyboard.add_button("&#128055;", color=VkKeyboardColor.POSITIVE)
            send_msg_with_keyboard("Какое животное нравится вам больше всего?", recipient_id, keyboard)
            self.answ_fourth_q.add(recipient_id)
            return
        if recipient_id not in self.answ_fifth_q:
            keyboard = VkKeyboard(inline=True)
            keyboard.add_button("0", color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button("1", color=VkKeyboardColor.POSITIVE)
            send_msg_with_keyboard("0 или 1?", recipient_id, keyboard)
            self.answ_fifth_q.add(recipient_id)
            return
        if recipient_id not in self.answ_sixth_q:
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("А мне откуда знать?", color=VkKeyboardColor.NEGATIVE)
            send_msg_with_keyboard("Чтобы еще спросить?....", recipient_id, keyboard)
            self.answ_sixth_q.add(recipient_id)
            return
        if recipient_id not in self.answ_seventh_q:
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("4", color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button("Налево", color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button("Я ФУТБОЛЬНЫЙ МЯЧИК", color=VkKeyboardColor.SECONDARY, )
            send_msg_with_keyboard("Загадка от Жака Фреско, на размышление четыре секунды...", recipient_id, keyboard)
            self.answ_seventh_q.add(recipient_id)
            return
        if recipient_id not in self.answ_eigth_q:
            keyboard = VkKeyboard(inline=True)
            keyboard.add_button("НЕ СКАЖУ", color=VkKeyboardColor.NEGATIVE)
            send_msg_with_keyboard("гДе Ты?", recipient_id, keyboard)
            self.answ_eigth_q.add(recipient_id)
            send_message("ПРИСТУПИМ К МЕМАМ", recipient_id)
            return
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("Мем", color=VkKeyboardColor.POSITIVE)
        memes = os.walk("memes/", topdown=False)


class MemSender:
    def __init__(self):
        self.users_and_memes = {}
        self.memes = []
        memes = os.walk("memes/", topdown=False)
        for mem in memes:
            self.memes.append(mem)

    def send_mem(self, recepient_id):
        self.add_user(recepient_id)
        image = random.choice(self.memes)
        while image in self.users_and_memes[recepient_id].liked_memes or\
                image in self.users_and_memes[recepient_id].disliked_memes:
            image = random.choice(self.memes)
        send_message("", recepient_id, "memes/" + random.choice(self.memes))

    def add_user(self, user_id):
        if user_id not in self.users_and_memes.keys():
            self.users_and_memes[user_id] = User()


token = "1d283b1a4b1377f88c8772397f3e67cf2a3bdc33468e314389bf9faa033f050369cad9b7f0bbcb2c78d08"
vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
vk_longpoll = VkLongPoll(vk_session)
quizier = Quizier()
mem_sender = MemSender()


def send_message(msg_text, recipient_id, photo=None):
    vk_session.method('messages.send', {'user_id': recipient_id, 'message': msg_text,
                                        'random_id': 0, 'attachment': ','.join(photo)})


def send_msg_with_keyboard(msg_text, recipient_id, keyboard):
    vk_session.method('messages.send', {'user_id': recipient_id, 'message': msg_text,
                                        'random_id': 0, 'keyboard': keyboard.get_keyboard()})


for event in vk_longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            sender_id = event.user_id
            if msg == "привет":
                send_message("Привет вездекодерам!", sender_id)
            elif msg == "мем":
                mem_sender.send_mem(sender_id)
            else:
                quizier.ask_question(sender_id)
