from app.photo import get_top_photos
from app.users import users_search, users_get


def cur_user(user_id):
    """Функция для получения параметров 3х фотографий"""

    dict_cur_user = users_get(user_id)
    for key in dict_cur_user.keys():
        dict = get_top_photos(key)
        for key2 in dict.keys():
            if 'photo_1_url' not in dict_cur_user[key]:
                dict_cur_user[key]['photo_1_url'] = dict[key2]['url']
                dict_cur_user[key]['photo_1_id'] = key2
                dict_cur_user[key]['photo_1_likes'] = dict[key2]['likes']
            elif 'photo_2_url' not in dict_cur_user[key]:
                dict_cur_user[key]['photo_2_url'] = dict[key2]['url']
                dict_cur_user[key]['photo_2_id'] = key2
                dict_cur_user[key]['photo_2_likes'] = dict[key2]['likes']
            else:
                dict_cur_user[key]['photo_3_url'] = dict[key2]['url']
                dict_cur_user[key]['photo_3_id'] = key2
                dict_cur_user[key]['photo_3_likes'] = dict[key2]['likes']
    return dict_cur_user


def search_people_and_photos(sex, age_at, age_to, city, status):
    """Функция для поиска людей и их фотографий"""

    dict_all_persons = users_search(sex, age_at, age_to, city, status)
    for key in dict_all_persons.keys():
        dict = get_top_photos(key)
        for key2 in dict.keys():
            if 'photo_1_url' not in dict_all_persons[key]:
                dict_all_persons[key]['photo_1_url'] = dict[key2]['url']
                dict_all_persons[key]['photo_1_id'] = key2
                dict_all_persons[key]['photo_1_likes'] = dict[key2]['likes']
            elif 'photo_2_url' not in dict_all_persons[key]:
                dict_all_persons[key]['photo_2_url'] = dict[key2]['url']
                dict_all_persons[key]['photo_2_id'] = key2
                dict_all_persons[key]['photo_2_likes'] = dict[key2]['likes']
            else:
                dict_all_persons[key]['photo_3_url'] = dict[key2]['url']
                dict_all_persons[key]['photo_3_id'] = key2
                dict_all_persons[key]['photo_3_likes'] = dict[key2]['likes']
    return dict_all_persons
