
from config.config import (access_token_group)
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
from random import randrange
import datetime

vkt = vk_api.VkApi(token=access_token_group)
longpoll = VkLongPoll(vkt)



def write_msg(user_id, message, attachment=None, keyboard = None):
    try:
        if attachment is not None:
            att = 'Прикреплены фото'
        else:
            att = 'Нет'

        print(f"""{datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')} -> Пользователю с ID {user_id} отправлено сообщение"{message}"
                     Вложения: {att}""")
        
        vkt.method('messages.send',
                  {'user_id': user_id,
                   'message': message,
                   'random_id': randrange(10 ** 7),
                   'attachment': attachment,
                   'keyboard': keyboard})
        
    except Exception as e:
        print(f"Error: {e}")


def edit_msg(user_id, message_id, message, attachment=None, keyboard=None):
    try:
        if attachment is not None:
            att = 'Прикреплены фото'
        else:
            att = 'Нет'

        print(f"""{datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')} -> Пользователю с ID {user_id} изменено сообщение"{message_id}"
                     Вложения: {att}""")
        
        vkt.method('messages.edit',
                  {'peer_id': user_id,
                   'message': message,
                   'message_id': message_id - 1,
                   'attachment': attachment,
                   'keyboard': keyboard})
        
    except Exception as e:
        print(f"Error: {e}")


def prepare_photo(user_id,photos,user_info):
    try:
        attachment = []
        if ('photo_1_url' in photos[max(photos)] is not None )or ('photo_2_url' in photos[max(photos)] is not None ) or ('photo_3_url' in photos[max(photos)] is not None):
            if 'photo_1_url' in photos[max(photos)] is not None:
                attachment.append(photos[max(photos)]['photo_1_url'])
            if 'photo_2_url' in photos[max(photos)] is not None:
                attachment.append(photos[max(photos)]['photo_2_url'])
            if 'photo_3_url' in photos[max(photos)] is not None:
                attachment.append(photos[max(photos)]['photo_3_url'])
        else:
            attachment = None

        text = f"""{user_info[max(user_info)]['first_name']} {user_info[max(user_info)]['last_name']}
        {user_info[max(user_info)]['link_pro']}"""
        photo = ''
        for att in range(1,len(attachment)+1):
            if photo == '':
                photo += 'photo'+str(user_info[user_id]['id'])+'_'+str(photos[max(photos)][f'photo_{att}_id'])
            else:
                photo += ',photo'+str(user_info[user_id]['id'])+'_'+str(photos[max(photos)][f'photo_{att}_id'])
        return text, photo
    except Exception as e:
        print(f"Error: {e}")
