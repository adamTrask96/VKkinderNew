from DB.connect import create_connect
from DB.create import creat_all_tables
from DB.insert import (add_users, add_users_and_search_params, add_favorites_users, add_black_list)
from DB.select import (select_search_params,select_one_user_for_view, select_favorites, select_blacklist,select_db_id_user)
from app.main_app import (search_people_and_photos, cur_user)
from functions import (event_listen,write_msg,prepare_photo)

connection = create_connect()

creat_all_tables(connection)

favorites = 1
black_list = 1
index = 1 

connection = create_connect() 


while 1: 
    message, user_id = event_listen()
    sex, city, dict_cur_user = cur_user(user_id)
    add_users(connection,dict_cur_user)
    age_at = 29
    age_to = 33
    status = 6
    db_id = select_db_id_user(connection,user_id)
    dict_favorites = select_favorites(connection,db_id[0])
    dict_blacklist = select_blacklist(connection,db_id[0])
    

    if message.lower() == "начать":
        name = dict_cur_user[user_id]['first_name']
        write_msg(user_id=user_id, message=f"""Привет, {name}! Введите 'поиск' для начала поиска анкет, для просмотра избранных анкет введите 'показать избранные анкеты', для просмотра черного списка введите 'показать черный список'""")


    elif message.lower() == "поиск":
        dict_all_questionnaires = search_people_and_photos(sex, age_at, age_to, city, status)
        add_users_and_search_params(connection,dict_all_questionnaires,sex,age_at,age_to,city,status)
        name = dict_cur_user[user_id]['first_name']
        write_msg(user_id, f"{name}, для просмотра анкет введите 'смотреть'")


    elif message.lower() == "смотреть":
        dict_for_watch = select_search_params(connection,sex,age_at,age_to,city,status)#
        if dict_for_watch == {}:
            write_msg(user_id, f"Записей для просмотра больше нет. Для повторного описка введите 'Поиск'")
        else:
            if index > len(dict_for_watch):
                index = 1
            dict_one_question = select_one_user_for_view(connection,dict_for_watch[index])
            text, photo = prepare_photo(dict_one_question)
            write_msg(user_id, text, photo)
            write_msg(user_id, "Для добавления в избранное введите 'добавить в избранное', для добавления в черный список введите 'добавить в черный список'")
            id_in_list = dict_one_question['bd_id']
            index+=1


    elif message.lower() == "добавить в избранное":
        text = add_favorites_users(connection, db_id[0], id_in_list)
        if text is not None:
            write_msg(user_id,text)
        else:
            name = dict_cur_user[user_id]['first_name']
            write_msg(user_id, f"{name}, для дальнейшего просмотра введите 'смотреть'")


    elif message.lower() == "добавить в черный список":
        text = add_black_list(connection, db_id[0], id_in_list)
        if text is not None:
            write_msg(user_id,text)
        else:
            name = dict_cur_user[user_id]['first_name']
            write_msg(user_id, f"{name}, для дальнейшего просмотра введите 'смотреть'")


    elif message.lower() == "показать избранные анкеты":
        if dict_favorites == []:
            write_msg(user_id, "У вас нет избранных анкет. Может добавим?")
        else:
            if favorites >= len(dict_favorites):
                write_msg(user_id, f"Избранные анкеты закончились. Для просмотра сначала введите 'с начала списка избранных'")
            else:
                dict_one_question = select_one_user_for_view(connection,dict_favorites[favorites][0])
                text, photo = prepare_photo(dict_one_question)
                write_msg(user_id, text, photo)
                favorites += 1


    elif message.lower() == "с начала списка избранных":
        favorites = 1
        write_msg(user_id, "для просмотра избранных анкет введите 'показать избранные анкеты'")


    elif message.lower() == "показать черный список":
        if dict_blacklist == {}:
            write_msg(user_id, "У вас нет анкет в ЧС. Может добавим?")
        else:
            if black_list >= len(dict_blacklist):
                write_msg(user_id, f"Анкеты в ЧС закончились. . Для просмотра сначала введите 'с начала черного списка'")
            else:
                dict_one_question = select_one_user_for_view(connection,dict_blacklist[black_list][0])
                text, photo = prepare_photo(dict_one_question)
                write_msg(user_id, text, photo)
                black_list += 1


    elif message.lower() == "с начала черного списка":
        black_list = 1
        write_msg(user_id, "Смотрим черный список?")


    elif message == "пока":
        write_msg(user_id, "Пока((")


    else:
        write_msg(user_id, "Не поняла вашего ответа...")

