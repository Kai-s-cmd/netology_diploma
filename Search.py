import json
import requests
from token_vk import personal_token as token
import vk_api
from vk_bot import VkBot

# Variables
access_token = token
vk = vk_api.VkApi(token=token)


class Search:
    """Bot getting info about user in VK"""
    def __init__(self, access_token, version='5.131'):
        self.token = access_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    # def _get_users_from_search(self):
    #     url = 'https://api.vk.com/method/users.search'
    #     params = {'age_from': }
    #     request = requests.get(url, params={**self.params, **params})
    #     user_info = json.loads(request.text)
    #     return user_info

    def _get_info_about_contacted_user_from_vk_id(self, user_id):
        """Функция получает данные из профиля пользователя."""
        response = vk.method('users.search', {'user_id': VkBot(user_id=user_id)})
        print(response)


