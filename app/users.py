from config.config import vk_access_token

import vk_api


def users_get(ids):
    """
    Возвращает расширенную информацию о пользователях.
    """
    all_persons = {}
    link_profile = 'https://vk.com/id'
    vk = vk_api.VkApi(token=vk_access_token)
    try:
        response = vk.method('users.get', {'user_ids': ids,
                                           'fields': 'verified, sex, bdate, city, home_town, has_photo, online, domain, nickname, screen_name, maiden_name, friend_status'})
        for item in response:
            all_persons[item['id']] = {'id': item['id']}
            for key in item.keys():
                if key == 'city':
                    all_persons[item['id']]['city_id'] = item[key]['id']
                    all_persons[item['id']]['city_title'] = item[key]['title']
                else:
                    all_persons[item['id']][key] = item[key]
            all_persons[item['id']]['link_pro'] = link_profile + str(item['id'])
    except Exception as e:
        print(f'Error occurred while getting users: {e}')
        return None
    return all_persons


def users_search(sex, age_at, age_to, city, status):
    ''' Возвращает список пользователей в соответствии с заданным критерием поиска.
    '''
    all_persons = {}
    link_profile = 'https://vk.com/id'
    vk = vk_api.VkApi(token=vk_access_token)
    try:
        response = vk.method('users.search', {'sort': 1,
                                              'sex': sex,
                                              'status': status,
                                              'age_from': age_at,
                                              'age_to': age_to,
                                              'has_photo': 1,
                                              'count': 50,
                                              'online': 1,
                                              'city': city})
        if 'items' not in response:
            raise ValueError('Response does not contain "items" key')
        for item in response['items']:
            if item.get("is_closed", False) == False:
                all_persons[item['id']] = {'id': item['id']}
                for key in item.keys():
                    if key == 'city':
                        all_persons[item['id']]['city_id'] = item[key]['id']
                        all_persons[item['id']]['city_title'] = item[key]['title']
                    else:
                        all_persons[item['id']][key] = item[key]
                all_persons[item['id']]['link_pro'] = link_profile + str(item['id'])
    except Exception as e:
        print(f'Error occurred while searching for users: {e}')
        return None
    return all_persons
