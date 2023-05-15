import vk_api
import pandas as pd
import datetime

from config.config import vk_access_token, access_token_group, group_id


def get_top_photos(owner_id):
    '''Функция возвращает топ 3 фотографии юзера по лайкам'''

    photos_dict = {}
    vk = vk_api.VkApi(token=vk_access_token)
    try:
        response = vk.method('photos.getAll', {'owner_id': owner_id,
                                               'extended': 1,
                                               'count': 200})
    except vk_api.ApiError as e:
        date = datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')
        print(f"""{date} -> Ошибка возврата фотографии: {e}""")
        return None

    for item in response['items']:
        try:
            m = 0
            for i in item['sizes']:
                if i['height'] > m:
                    m = i['height']
                    url = i['url']
            photos_dict[item['id']] = {'url': url,
                                       'likes': item['likes']['count']}
        except KeyError as e:
            date = datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')
            print(f"{date} -> Ошибка процесса выгрузки фото: {e}")
            continue

    df = pd.DataFrame(photos_dict)
    data = df.transpose()
    data = data.sort_values(by='likes', ascending=False)
    top_photos = data.head(3)
    return top_photos.to_dict('index')


def get_messages_upload_server():
    '''Возвращает URL-адрес сервера загрузки групповых сообщений'''
    vk = vk_api.VkApi(token=access_token_group)
    try:
        response = vk.method('photos.getMessagesUploadServer',
                             {'group_id': group_id})
    except vk_api.ApiError as e:
        date = datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')
        print(f"{date} -> Ошибка выгрузки: {e}")
        return None
    return response
