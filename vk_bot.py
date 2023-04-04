from random import randrange
from token_vk import bot_token, personal_token
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from search_users import Search
from bot_db import VkDB
from vk_api.exceptions import ApiError


class VkBot:
    """VK бот получающий информацию о пользователе,
       для дальнейшего поиска пары."""
    def __init__(self, user_id):
        self.search = Search(personal_token)
        self.database = VkDB()
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)
        self._COMMANDS = ['ПРИВЕТ', "ДАЛЕЕ", 'ПОКА', 'ПОМОЩЬ']
        self._BIRTH_YEAR = self.search.get_info_about_contacted_user_from_vk_id(user_id)[0]
        self._CITY_ID = self.search.get_info_about_contacted_user_from_vk_id(user_id)[2]
        self._AGE_FROM = self._BIRTH_YEAR - 5
        self._AGE_TO = self._BIRTH_YEAR + 5
        self._SEX = self.search.get_info_about_contacted_user_from_vk_id(self._USER_ID)[1]

    def _get_user_name_from_vk_id(self, user_id):
        """Функция получает имя пользователя"""
        response = vk.method('users.get', {'user_id': user_id})
        return response[0]["first_name"] + ' ' + response[0]["last_name"]

    def write_msg(self, user_id, message, attachment=None):
        try:
            vk.method('messages.send', {'user_id': user_id,
                                        'message': message,
                                        'attachment': attachment,
                                        'random_id': randrange(10 ** 7)
                                        })
        except ApiError:
            return

    def new_message(self, message):
        if message.upper() == self._COMMANDS[0]:
            return f'Привет, {self._USERNAME}!'
        elif message.upper() == self._COMMANDS[1]:
            if self._CITY_ID is None:
                self.write_msg(event.user_id, 'Город не указан.\n'
                    'Вы видите эту надпись потому что в вашем профиле не указан город.\n'
                    'Напишите город для поиска, в формате "Город Москва":')
            if self._BIRTH_YEAR is None:
                self.write_msg(event.user_id,
                               'Не хватает информации о вашей дате рождения. '
                               'Укажите ваш год рождения, в формате "год 1990"')

            try:
                # Создает стол в дб
                self.database.create_db()
                # Для женского пола подбирает мужчин.
                if self._SEX == 1:
                    self._SEX = 2
                # Для мужского пола подбирает женщин.
                elif self._SEX == 2:
                    self._SEX = 1
                for user in self.search.search_users(self._CITY_ID,
                                                     self._AGE_FROM,
                                                     self._AGE_TO,
                                                     self._SEX,
                                                     31):
                    print(user)
                    name = user['name']
                    id = user['id']
                    # Проверка не просмотрен ли уже пользователь
                    if self.database.find_client(self._USER_ID, sort_id=id):
                        continue
                    else:
                        # Добавляет в имя и айди, а также айди контактирующего в дб
                        self.database.add_client(self._USER_ID, id, name)
                        self.write_msg(event.user_id, f'https://vk.com/id{id}')
                        self.write_msg(event.user_id, name)
                        for photo in self.search.photos_get(id):
                            media = f"photo{id}_{photo}"
                            self.write_msg(event.user_id, 'Фото',
                                           attachment=media)
                        break
            except TypeError:
                return

        elif message.upper() == self._COMMANDS[2]:
            return f'До скорой встречи, {self._USERNAME}!'
        elif message.upper() == self._COMMANDS[-1]:
            return f'Команды бота:\n' \
                   f'далее - посмотреть следующую анкету\n' \
                   f'помощь - выдает список команд.\n' \
                   f'для старта напишите привет:)\n' \
                   f'чтобы указать город вручную введите "Город Москва"\n' \
                   f'чтобы указать год вручную введите "год 1990"'
        elif 'город'.upper() in message.upper():
            city_info = message.upper().split(' ')
            self._CITY_ID = city_info[1]
        elif 'год'.upper() in message.upper():
            year_info = message.upper().split(' ')
            self._BIRTH_YEAR = year_info[1]
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
