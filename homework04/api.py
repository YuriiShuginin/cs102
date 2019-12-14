import requests
import time

from typing import List, Dict, Optional
from config import VK_CONFIG as vk


def get(url: str, params={}, timeout=5, max_retries=5, backoff_factor=0.3) -> Optional[requests.models.Response]:
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for i in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=(timeout, 3))
            return response
        except requests.exceptions.RequestException:
            if i == max_retries - 1:
                raise
            delay = backoff_factor * 2 ** i
            time.sleep(delay)


def get_friends(user_id, fields='bdate') -> Dict:
    """ Вернуть данных о друзьях пользователя
    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    query_params = {
        'access_token': vk['access_token'],
        'user_id': user_id,
        'fields': fields,
        'v': vk['version']
    }

    url = "https://api.vk.com/method/friends.get?"
    response = get(url, query_params)

    return response.json()['response']['items']