from random import randrange
from token_vk import bot_token
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
# from Search import VkBot

# Variable


class VkBot:
    """VK бот спрашивающий информацию о пользователе,
       для дальнейшего поиска пары."""
    def __init__(self, user_id):
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)
        self._COMMANDS = ['ПРИВЕТ', "ЗАПОЛНИТЬ АНКЕТУ", 'ПОКА']

    def _get_user_name_from_vk_id(self, user_id):
        """Функция получает имя пользователя"""
        response = vk.method('users.get', {'user_id': user_id})
        print(response)
        return response[0]["first_name"] + ' ' + response[0]["last_name"]

    def write_msg(self, user_id, message):
        vk.method('messages.send', {'user_id': user_id, 'message': message,
                                    'random_id': randrange(10 ** 7)})

    def new_message(self, message):
        if message.upper() == self._COMMANDS[0]:
            return f'Привет, {self._USERNAME}!'
        elif message.upper() == self._COMMANDS[1]:
            return f'Заполните анкету, {self._USERNAME}.'
        elif message.upper() == self._COMMANDS[2]:
            return f'До скорой встречи, {self._USERNAME}!'
        else:
            return 'Не понимаю о чем вы...'


if __name__ == '__main__':
    vk = vk_api.VkApi(token=bot_token)
    longpoll = VkLongPoll(vk)

    for event in longpoll.listen():
        # Если пришло новое сообщение
        if event.type == VkEventType.MESSAGE_NEW:
            # Если оно имеет метку для бота
            if event.to_me:
                # Сообщение от пользователя
                print(f'New message from {event.user_id}', end='\n')
                bot = VkBot(event.user_id)
                bot.write_msg(event.user_id, bot.new_message(event.text))
    #
    # @staticmethod
    # def _clean_all_tag_from_str(string_line):
    #     """
    #     Очистка строки stringLine от тэгов и их содержимых
    #     :param string_line: Очищаемая строка
    #     :return: очищенная строка
    #     """
    #
    #     result = ""
    #     not_skip = True
    #     for i in list(string_line):
    #         if not_skip:
    #             if i == "<":
    #                 not_skip = False
    #             else:
    #                 result += i
    #         else:
    #             if i == ">":
    #                 not_skip = True
    #
    #     return result