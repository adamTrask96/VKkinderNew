from config.imports import *
from vk_api.longpoll import VkLongPoll, VkEventType


vkt = vk_api.VkApi(token=access_token_group)
longpoll = VkLongPoll(vkt)


def event_listen() -> object:
    for event in longpoll.listen():
        try:
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    message = event.text.lower()
                    return message, event.user_id
        except Exception as e:
            print(f"Error: {e}")


def write_msg(user_id, message, attachment=None):
    try:
        if attachment is not None:
            att = 'Прикреплены фото'
        else:
            att = 'Нет'
        print(f'''Пользователю с ID {user_id} отправлено сообщение"{message}"
        Вложения: {att}''')
        vkt.method('messages.send',
                  {'user_id': user_id,
                   'message': message,
                   'random_id': randrange(10 ** 7),
                   'attachment': attachment})
    except Exception as e:
        print(f"Error: {e}")


def prepare_photo(dict_all_persons):
    try:
        if 'photo_1_url' in dict_all_persons is not None and 'photo_2_url' in dict_all_persons is not None and 'photo_3_url' in dict_all_persons is not None:
            attachment = [dict_all_persons['photo_1_url'], dict_all_persons['photo_2_url'],dict_all_persons['photo_3_url']]
        elif 'photo_1_url' in dict_all_persons is not None and 'photo_2_url' in dict_all_persons is not None and 'photo_3_url' in dict_all_persons is None:
            attachment = [dict_all_persons['photo_1_url'], dict_all_persons['photo_2_url']]
        elif 'photo_1_url' in dict_all_persons is not None and 'photo_2_url' in dict_all_persons is None and 'photo_3_url' in dict_all_persons is None:
            attachment = [dict_all_persons['photo_1_url']]
        else:
            attachment = None
        text = f"""{dict_all_persons['first_name']} {dict_all_persons['last_name']}
        {dict_all_persons['link_pro']}"""
        photo = ''
        for att in range(1,len(attachment)+1):
            if photo == '':
                photo += 'photo'+str(dict_all_persons['id'])+'_'+str(dict_all_persons[f'photo_{att}_id'])
            else:
                photo += ',photo'+str(dict_all_persons['id'])+'_'+str(dict_all_persons[f'photo_{att}_id'])
        return text, photo
    except Exception as e:
        print(f"Error: {e}")
