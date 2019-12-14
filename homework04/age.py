import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    
    friends = get_friends(user_id)
    ages = []
    for friend in friends:
        user = User(**friend)
        try:
            bdate = str(user.bdate)
            bd, bm, by = map(int, bdate.split('.'))
            today = dt.date.today()
            ages.append(today.year - by - ((today.month, today.day) < (bm, bd)))
        except ValueError:
            pass
    try:
        return median(ages)
    except:
        pass