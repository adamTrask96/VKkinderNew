from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

token = input('Token: ')
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

def write_msg(user_id, message):
    try:
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})
    except vk_api.exceptions.ApiError as e:
        print(f"Failed to send message: {e}")

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            try:
                request = event.text
            except AttributeError:
                continue
            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
