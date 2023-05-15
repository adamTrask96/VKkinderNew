from functions import (write_msg,
                       prepare_photo)

from DB.update import (update_leave_in_Black_list,
                       update_leave_in_Favorite_list,
                       update_age_at_params,
                       update_age_to_params,
                       update_sex_params)

from DB.select import (select_find_user_in_DB,
                       select_params_of_user,
                       select_user_in_black,
                       select_user_in_favorite)

from DB.insert import (insert_Dislike_user,
                       insert_favorite_user,
                       insert_new_user_and_insert_params,
                       insert_watched_user)

from app.users import (users_search,
                       users_get)

from app.main_app import cur_user

from config.config import (access_token_group)
from vk_api.longpoll import VkLongPoll, VkEventType

import vk_api
import vk_api.keyboard


vkt = vk_api.VkApi(token=access_token_group)
longpoll = VkLongPoll(vkt)


def function_of_new_message() -> str:
    """
    Функция как отдельный поток прослушивания вк сообщений
    Функция необходима для паралельной прослушки (меньше строк кода)
    :::ВХОДНЫЕ ПАРАМЕТРЫ\n
    Отсутсвуют
    :::ВЫХОДНЫЕ ПАРАМЕТРЫ\n
    Текст сообщения
    """
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                return event.text.lower()


# Главная функция!
def main():
    find_users = []
    id_prosmotr = 0
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                message = event.text.lower()
                if message.lower() == "начать":
                    mark = vk_api.keyboard.VkKeyboard()
                    mark.add_button("Поиск")

                    write_msg(user_id=event.user_id,
                              message="""Привет!
    Я помогу тебе найти друзей в твоем городе!
    Для начало, нажми на кнопку "Поиск".""",
                              keyboard=mark.get_keyboard())

                elif message.lower() == "поиск":
                    write_msg(user_id=event.user_id,
                              message="Воу, я вижу ты готов к поиску, тогда мы приступаем!")

                    if select_params_of_user(event.user_id) is None:
                        mark = vk_api.keyboard.VkKeyboard()
                        write_msg(user_id=event.user_id,
                                  message="""Для начала, давай познакомимся!
Пришли мне сообщение о тебе в таком формате!
-------------------------
    Возраст от: 29
    Возраст до: 30
    Пол: 1
    Семейное положение: 1
-------------------------
    """,
                                  keyboard=mark.get_empty_keyboard())

                        message = function_of_new_message()

                        if insert_new_user_and_insert_params(user_id=event.user_id,
                                                             text=message):
                            write_msg(user_id=event.user_id,
                                      message="Супер! Теперь можно работать!")

                    user = select_params_of_user(event.user_id)
                    if user is not None:
                        write_msg(user_id=event.user_id,
                                  message="Приступаем к поиску")

                        users = users_search(user[2], user[0], user[1], user[3], user[4])

                        for i in users:
                            find_users.append(i)

                        write_msg(user_id=event.user_id,
                                  message="Я готов! Начинаем просмотр!")

                        """ Создание инофрмации о пользователе и его фото"""
                        while len(find_users) > 0:
                            if select_find_user_in_DB(event.user_id, find_users[id_prosmotr]):
                                find_users.remove(find_users[id_prosmotr])
                            else:
                                break

                        id_prosmotr = 0
                        user_info = users_get(find_users[id_prosmotr])
                        photo = cur_user(find_users[id_prosmotr])
                        text, photo = prepare_photo(find_users[id_prosmotr], photo, user_info)

                        mark = vk_api.keyboard.VkKeyboard()
                        mark.add_button('👍')
                        mark.add_button('👎')
                        mark.add_button('Дальше')
                        mark.add_button('Закончить')

                        write_msg(user_id=event.user_id,
                                  message=text,
                                  attachment=photo,
                                  keyboard=mark.get_keyboard())

                elif message.lower() == "дальше":
                            if insert_watched_user(event.user_id, find_users[id_prosmotr]):
                                id_prosmotr += 1
                                user_info = users_get(find_users[id_prosmotr])
                                photo = cur_user(find_users[id_prosmotr])
                                text, photo = prepare_photo(find_users[id_prosmotr], photo, user_info)

                                write_msg(user_id=event.user_id,
                                          message=text,
                                          attachment=photo)

                elif message.lower() == "👍":
                            if insert_favorite_user(event.user_id, find_users[id_prosmotr]):
                                id_prosmotr += 1
                                user_info = users_get(find_users[id_prosmotr])
                                photo = cur_user(find_users[id_prosmotr])
                                text, photo = prepare_photo(find_users[id_prosmotr], photo, user_info)

                                write_msg(user_id=event.user_id,
                                          message=text,
                                          attachment=photo)

                elif message.lower() == "👎":
                            if insert_Dislike_user(event.user_id, find_users[id_prosmotr]):
                                id_prosmotr += 1
                                user_info = users_get(find_users[id_prosmotr])
                                photo = cur_user(find_users[id_prosmotr])
                                text, photo = prepare_photo(find_users[id_prosmotr], photo, user_info)

                                write_msg(user_id=event.user_id,
                                          message=text,
                                          attachment=photo)

                elif message.lower() == "закончить":
                    id_prosmotr = 0
                    mark = vk_api.keyboard.VkKeyboard(one_time=True)
                    mark.add_button("Смотреть лайки")
                    mark.add_button("Смотреть дизлайки")
                    mark.add_button("Настроить параметры поиска")
                    mark.add_button("Поиск")

                    write_msg(user_id=event.user_id,
                              message="Хорошо! Что хотите сделать?",
                              keyboard=mark.get_keyboard())

                elif message.lower() == "смотреть лайки":
                    find_users = select_user_in_favorite(event.user_id)

                    if len(find_users) != 0:

                        write_msg(user_id=event.user_id,
                                  message=f"Ого! У вас {len(find_users)} пользователей в Лайках! Погнали смотреть...")

                        index = 0
                        user = find_users[0][index]

                        user_info = users_get(user)
                        photo = cur_user(user)
                        text, photo = prepare_photo(user, photo, user_info)

                        mark = vk_api.keyboard.VkKeyboard()
                        mark.add_button("Убрать Лайк")
                        mark.add_button("Дальше")
                        mark.add_button("Закончить")

                        write_msg(user_id=event.user_id,
                                  message=text,
                                  attachment=photo,
                                  keyboard=mark.get_keyboard())

                        message = function_of_new_message()
                        while message != "закончить":
                            if message == "убрать лайк":
                                user = find_users[0]
                                if update_leave_in_Favorite_list(event.user_id, user):
                                    if index < len(find_users)-1:
                                        find_users = select_user_in_favorite(event.user_id)
                                        user = find_users[index]
                                        user = user[0]

                                        user_info = users_get(user)
                                        photo = cur_user(user)
                                        text, photo = prepare_photo(user, photo, user_info)

                                        write_msg(user_id=event.user_id,
                                                  message=text,
                                                  attachment=photo)

                                        message = function_of_new_message()

                                    else:
                                        find_users = select_user_in_favorite(event.user_id)

                                        if len(find_users) == 0:
                                            mark = vk_api.keyboard.VkKeyboard(one_time=True)
                                            mark.add_button("Смотреть лайки")
                                            mark.add_button("Смотреть дизлайки")
                                            mark.add_button("Настроить параметры поиска")
                                            mark.add_button("Поиск")

                                            write_msg(event.user_id, "Пользователи закончились!",
                                                      keyboard=mark.get_keyboard())
                                            break

                                        else:
                                            write_msg(event.user_id, "Пользователи закончились! Идем по кругу")

                                            index = 0
                                            user = find_users[index]
                                            user = user[0]

                                            user_info = users_get(user)
                                            photo = cur_user(user)
                                            text, photo = prepare_photo(user, photo, user_info)

                                            write_msg(user_id=event.user_id,
                                                      message=text,
                                                      attachment=photo)

                                            message = function_of_new_message()

                            elif message == "дальше":
                                if index < len(find_users) - 1:
                                    index += 1
                                    user = find_users[index]
                                    user = user[0]

                                    user_info = users_get(user)
                                    photo = cur_user(user)
                                    text, photo = prepare_photo(user, photo, user_info)

                                    write_msg(user_id = event.user_id,
                                              message = text,
                                              attachment = photo)
                                                        
                                    message = function_of_new_message()
                                                                    
                                else:
                                    if len(find_users) == 0:
                                        mark = vk_api.keyboard.VkKeyboard(one_time=True)
                                        mark.add_button("Смотреть лайки")
                                        mark.add_button("Смотреть дизлайки")
                                        mark.add_button("Настроить параметры поиска")
                                        mark.add_button("Поиск")

                                        write_msg(event.user_id, "Пользователи закончились!",keyboard = mark.get_keyboard())
                                                        
                                    else:
                                        write_msg(event.user_id, "Пользователи закончились! Идем по кругу")
                                                                    
                                        index = 0
                                        user = find_users[index]
                                        user = user[0]
                                                                    
                                        user_info = users_get(user)
                                        photo = cur_user(user)
                                        text, photo = prepare_photo(user, photo, user_info)

                                        write_msg(user_id = event.user_id,
                                                  message = text,
                                                  attachment = photo)
                                                            
                                        message = function_of_new_message()

                            else:
                                write_msg(event.user_id, "Не поняла вашего ответа...")                        

                        mark = vk_api.keyboard.VkKeyboard(one_time=True)
                        mark.add_button("Смотреть лайки")
                        mark.add_button("Смотреть дизлайки")
                        mark.add_button("Настроить параметры поиска")
                        mark.add_button("Поиск")

                        write_msg(user_id=event.user_id,
                                  message="Хорошо! Что хотите сделать?",
                                  keyboard=mark.get_keyboard())

                    else:
                        find_users = []
                        mark = vk_api.keyboard.VkKeyboard(one_time=True)
                        mark.add_button("Смотреть лайки")
                        mark.add_button("Смотреть дизлайки")
                        mark.add_button("Настроить параметры поиска")
                        mark.add_button("Поиск")

                        write_msg(user_id=event.user_id,
                                  message="У вас нет пользователей с лайками!",
                                  keyboard=mark.get_keyboard())

                elif message.lower() == "смотреть дизлайки":
                    find_users = select_user_in_black(event.user_id)

                    if len(find_users) != 0:

                        write_msg(user_id=event.user_id,
                                  message=f"Ого! У вас {len(find_users)} пользователей в Дизах! Погнали смотреть...")

                        index = 0
                        user = find_users[0][index]

                        user_info = users_get(user)
                        photo = cur_user(user)
                        text, photo = prepare_photo(user, photo, user_info)

                        mark = vk_api.keyboard.VkKeyboard()
                        mark.add_button("Убрать Диз")
                        mark.add_button("Дальше")
                        mark.add_button("Закончить")

                        write_msg(user_id=event.user_id,
                                  message=text,
                                  attachment=photo,
                                  keyboard=mark.get_keyboard())

                        message = function_of_new_message()
                        while message != "закончить":
                            if message == "убрать диз":
                                user = find_users[0]
                                if update_leave_in_Black_list(event.user_id,user):
                                    if index < len(find_users)-1:
                                        find_users = select_user_in_black(event.user_id)
                                        user = find_users[index]
                                        user = user[0]

                                        user_info = users_get(user)
                                        photo = cur_user(user)
                                        text, photo = prepare_photo(user, photo, user_info)

                                        write_msg(user_id=event.user_id,
                                                  message=text,
                                                  attachment=photo)

                                        message = function_of_new_message()

                                    else:
                                        if len(find_users) == 0:
                                            mark = vk_api.keyboard.VkKeyboard(one_time=True)
                                            mark.add_button("Смотреть лайки")
                                            mark.add_button("Смотреть дизлайки")
                                            mark.add_button("Настроить параметры поиска")
                                            mark.add_button("Поиск")

                                            write_msg(event.user_id, "Пользователи закончились!",keyboard = mark.get_keyboard())
                                            break

                                        write_msg(event.user_id, "Пользователи закончились! Идем по кругу")

                                        index = 0
                                        user = find_users[index]
                                        user = user[0]

                                        user_info = users_get(user)
                                        photo = cur_user(user)
                                        text, photo = prepare_photo(user, photo, user_info)

                                        write_msg(user_id=event.user_id,
                                                  message=text,
                                                  attachment=photo)

                            elif message == "дальше":
                                if index < len(find_users) - 1:

                                    index += 1
                                    user = find_users[index]
                                    user = user[0]

                                    user_info = users_get(user)
                                    photo = cur_user(user)
                                    text, photo = prepare_photo(user, photo, user_info)

                                    write_msg(user_id=event.user_id,
                                              message=text,
                                              attachment=photo)

                                    message = function_of_new_message()

                                else:
                                    if len(find_users) == 0:
                                        mark = vk_api.keyboard.VkKeyboard(one_time=True)
                                        mark.add_button("Смотреть лайки")
                                        mark.add_button("Смотреть дизлайки")
                                        mark.add_button("Настроить параметры поиска")
                                        mark.add_button("Поиск")

                                        write_msg(event.user_id, "Пользователи закончились!",
                                                  keyboard=mark.get_keyboard())

                                        break

                                    write_msg(event.user_id, "Пользователи закончились! Идем по кругу")

                                    index = 0
                                    user = find_users[index]
                                    user = user[0]

                                    user_info = users_get(user)
                                    photo = cur_user(user)
                                    text, photo = prepare_photo(user, photo, user_info)

                                    write_msg(user_id=event.user_id,
                                              message=text,
                                              attachment=photo)

                                    message = function_of_new_message()

                            else:
                                write_msg(event.user_id, "Не поняла вашего ответа...")

                        mark = vk_api.keyboard.VkKeyboard(one_time=True)
                        mark.add_button("Смотреть лайки")
                        mark.add_button("Смотреть дизлайки")
                        mark.add_button("Настроить параметры поиска")
                        mark.add_button("Поиск")

                        write_msg(user_id=event.user_id,
                                  message="Хорошо! Что хотите сделать?",
                                  keyboard=mark.get_keyboard())

                    else:
                        find_users = []
                        mark = vk_api.keyboard.VkKeyboard(one_time=True)
                        mark.add_button("Смотреть лайки")
                        mark.add_button("Смотреть дизлайки")
                        mark.add_button("Настроить параметры поиска")
                        mark.add_button("Поиск")
                        write_msg(user_id=event.user_id,
                                  message="У вас нет пользователей с дизами!",
                                  keyboard=mark.get_keyboard())

                elif message.lower() == "настроить параметры поиска":
                    mark = vk_api.keyboard.VkKeyboard(inline=True)
                    mark.add_button("Возрост от")
                    mark.add_button("Возрост до")
                    mark.add_line()
                    mark.add_button("Пол")
                    mark.add_button("Назад")

                    write_msg(event.user_id, 
                              "Хорошо, скажите, что бы вы хотели исправить?",
                              keyboard=mark.get_keyboard())

                    param_user = select_params_of_user(event.user_id)

                    message = function_of_new_message()
                    if message == "возрост от":
                        write_msg(user_id=event.user_id,
                                  message="Введите новое значение начального возроста",
                                  keyboard=mark.get_empty_keyboard())

                        number = function_of_new_message()
                        if int(number)>0 and int(number)<100 and int(number)<int(param_user[0]):
                            update_age_at_params(event.user_id,int(number))
                            mark = vk_api.keyboard.VkKeyboard(one_time=True)
                            mark.add_button("Смотреть лайки")
                            mark.add_button("Смотреть дизлайки")
                            mark.add_button("Настроить параметры поиска")
                            mark.add_button("Поиск")
                            write_msg(user_id=event.user_id,
                                      message="Что будем делать?",
                                      keyboard=mark.get_keyboard())

                        else:
                            mark = vk_api.keyboard.VkKeyboard(one_time=True)
                            mark.add_button("Смотреть лайки")
                            mark.add_button("Смотреть дизлайки")
                            mark.add_button("Настроить параметры поиска")
                            mark.add_button("Поиск")
                            write_msg(user_id=event.user_id,
                                      message="Начальный возраст привышает конечный",
                                      keyboard=mark.get_keyboard())                                                    

                    elif message == "возрост до":
                        write_msg(user_id=event.user_id,
                                  message="Введите новое значение конечного возроста",
                                  keyboard=mark.get_empty_keyboard())

                        number = function_of_new_message()
                        if int(number)>0 and int(number)<100:
                            update_age_to_params(event.user_id,int(number))
                            mark = vk_api.keyboard.VkKeyboard(one_time=True)
                            mark.add_button("Смотреть лайки")
                            mark.add_button("Смотреть дизлайки")
                            mark.add_button("Настроить параметры поиска")
                            mark.add_button("Поиск")
                            write_msg(user_id=event.user_id,
                                      message="Что будем делать?",
                                      keyboard=mark.get_keyboard())

                    elif message == "пол":
                        sex = select_params_of_user(event.user_id)[2]
                        if sex == 1:
                            sex = 2
                        else:
                            sex = 1

                        update_sex_params(event.user_id, sex)
                        mark = vk_api.keyboard.VkKeyboard(one_time=True)
                        mark.add_button("Смотреть лайки")
                        mark.add_button("Смотреть дизлайки")
                        mark.add_button("Настроить параметры поиска")
                        mark.add_button("Поиск")
                        write_msg(user_id=event.user_id,
                                  message="Что будем делать?",
                                  keyboard=mark.get_keyboard())

                    elif message == "назад":
                        mark = vk_api.keyboard.VkKeyboard(one_time=True)
                        mark.add_button("Смотреть лайки")
                        mark.add_button("Смотреть дизлайки")
                        mark.add_button("Настроить параметры поиска")
                        mark.add_button("Поиск")

                        write_msg(user_id=event.user_id,
                                  message="Хорошо! Что хотите сделать?",
                                  keyboard=mark.get_keyboard())

                else:
                    write_msg(event.user_id, "Не поняла вашего ответа...")


if __name__ == "__main__":
    main()
