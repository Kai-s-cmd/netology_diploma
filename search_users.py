import vk_api
from vk_api.exceptions import ApiError
import itertools

# Variables


class Search:
    """Bot getting info about user in VK"""
    def __init__(self, token):
        self.vk_api = vk_api.VkApi(token=token)

    def get_info_about_contacted_user_from_vk_id(self, user_id):
        """Функция получает данные из профиля пользователя."""
        try:
            response = self.vk_api.method('users.get',
                                          {'user_id': user_id,
                                           'fields': 'city, sex, bdate'})
            print(response)
        except ApiError:
            return

        return response

    def search_users(self, city_id, age_from, age_to, sex, offset=None):
        """Функция ищет пользователей похожих на
        контактирующего пользователя по заданным параметрам"""
        try:
            profiles = self.vk_api.method('users.search',
                                          {'city_id': city_id,
                                           'age_from': age_from,
                                           'age_to': age_to,
                                           'sex': sex,
                                           'count': 30,  # выдает по 30 анкет
                                           'status': 6,  # в активном поиске
                                           'offset': offset})
        except ApiError:
            return

        profiles = profiles['items']
        result = []
        for profile in profiles:
            if profile['is_closed'] is False:
                result.append({'name': profile['first_name'] + ' '
                               + profile['last_name'], 'id': profile['id']})
        return result

    def photos_get(self, user_id):
        response = self.vk_api.method('photos.get', {'album_id': 'profile',
                                                     'owner_id': user_id,
                                                     'extended': 1})

        ids = []
        likes_count = []
        for item in response['items']:
            for params, value in item.items():
                if params == 'id':
                    ids.append(value)
                if params == "likes":
                    for likes, number in value.items():
                        if likes == "count":
                            likes_count.append(number)
        # Соединяет лист с ID и лист с likes в словарь
        top_numbers_of_likes = {ids[i]: likes_count[i] for i in
                                range(len(ids))}
        # Сортирует словаль по лайкам
        top_numbers_of_likes = {k: v for k, v in sorted(
            top_numbers_of_likes.items(), key=lambda item: item[1],
            reverse=True)}
        # Делит словарь и выдает первые 3 значения, где ключ это id, а value
        # это лайки.
        top_numbers_of_likes = dict(itertools.islice(top_numbers_of_likes.items(),
                                                     0, 3))
        return top_numbers_of_likes
