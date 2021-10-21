from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode
import requests
from django.utils import timezone
from social_core.exceptions import AuthException, AuthForbidden
from users.models import UserProfile


# скрипт, кот. при авторизации срабатывает и идет в вк на страницу авторизованного пользователя и берет оттуда данные
def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return
    # получаем api_url, кот. обратится к VK, передаст параметры и получит ответ
    api_url = urlunparse(('http', 'api.vk.com', '/method/users.get', None, urlencode(
        OrderedDict(fields=','.join(('bdate', 'sex', 'about')), access_token=response['access_token'],
                    v=5.131)), None))
    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0] # Получаем всю инфу, кот. нам пришла

    if data['sex'] == 2:
        user.userprofile.gender = UserProfile.MALE
    elif data['sex'] == 1:
        user.userprofile.gender = UserProfile.FEMALE
    else:
        pass

    if data['about']:
        user.userprofile.about = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().date().year - bdate.year
        user.age = age
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    user.save()
