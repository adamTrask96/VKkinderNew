from DB.connect import create_connect
from functions import write_msg
from psycopg2 import Error

import datetime

"""
Файлик для изменения данных в какой-то либо таблице! 
"""

def update_leave_in_Black_list(user_id,find_id) -> bool:
    """
    Функция убирает пользователя из базы черного списка. Однако, не убирает из просмотренных!
    :::ВХОДНЫЕ ДАННЫЕ\n
    user_id -> главный пользователь\n
    find_id -> поисковой пользователь\n
    :::ВЫХОДНЫЕ ДАННЫЕ\n
    True если удалил
    False если не удалил
    """

    db_connect = create_connect()
    cursor = db_connect.cursor()
    
    try:
        cursor.execute("UPDATE users SET likes = 0 WHERE main_user = %s and find_user = %s",(user_id,find_id))
        db_connect.commit()
        db_connect.close()

        write_msg(user_id = user_id,
                      message = "ДизЛайк убран! Идем дальше...")
        
        return True
    
    except Error as error:
        # Сообщение в логи
        print(f"""{datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')}: Произошла ошибка обновления таблицы!
Текст ошибки: {error.pgerror}
Код ошбики: {error.pgcode}""")

        # Сообщение пользователю 
        write_msg(user_id = user_id,
                      message = "Вовремя удаления произошла ошибка, дизлайк не убран!")
        
        db_connect.close()
        return False

def update_sex_params(user_id,sex) -> bool:
    """
    Функция убирает пользователя из базы белого списка. Однако, не убирает из просмотренных!
    :::ВХОДНЫЕ ДАННЫЕ\n
    user_id -> главный пользователь\n
    sex -> новый поиск\n
    :::ВЫХОДНЫЕ ДАННЫЕ\n
    True если удалил
    False если не удалил
    """

    db_connect = create_connect()
    cursor = db_connect.cursor()
    
    try:
        cursor.execute("UPDATE find_params SET sex = %s WHERE main_user = %s",(sex,user_id))
        db_connect.commit()
        db_connect.close()

        write_msg(user_id = user_id,
                      message = "Параметр пола изменен!")
        
        return True
    
    except Error as error:
        # Сообщение в логи
        print(f"""{datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')}: Произошла ошибка обновления таблицы!
Текст ошибки: {error.pgerror}
Код ошбики: {error.pgcode}""")

        # Сообщение пользователю 
        write_msg(user_id = user_id,
                      message = "Вовремя изменения произошла ошибка")
        
        db_connect.close()
        return False

def update_age_at_params(user_id,age_ate) -> bool:
    """
    Функция убирает пользователя из базы белого списка. Однако, не убирает из просмотренных!
    :::ВХОДНЫЕ ДАННЫЕ\n
    user_id -> главный пользователь\n
    age_ate -> начальный\n
    :::ВЫХОДНЫЕ ДАННЫЕ\n
    True если удалил
    False если не удалил
    """

    db_connect = create_connect()
    cursor = db_connect.cursor()
    
    try:
        cursor.execute("UPDATE find_params SET age_from = %s WHERE main_user = %s",(age_ate,user_id))
        db_connect.commit()
        db_connect.close()

        write_msg(user_id = user_id,
                      message = "Начальный возраст изменен!")
        
        return True
    
    except Error as error:
        # Сообщение в логи
        print(f"""{datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')}: Произошла ошибка обновления таблицы!
Текст ошибки: {error.pgerror}
Код ошбики: {error.pgcode}""")

        # Сообщение пользователю 
        write_msg(user_id = user_id,
                      message = "Вовремя изменения произошла ошибка")
        
        db_connect.close()
        return False

def update_age_to_params(user_id,age_to) -> bool:
    """
    Функция убирает пользователя из базы белого списка. Однако, не убирает из просмотренных!
    :::ВХОДНЫЕ ДАННЫЕ\n
    user_id -> главный пользователь\n
    sex -> новый поиск\n
    :::ВЫХОДНЫЕ ДАННЫЕ\n
    True если удалил
    False если не удалил
    """

    db_connect = create_connect()
    cursor = db_connect.cursor()
    
    try:
        cursor.execute("UPDATE find_params SET age_to = %s WHERE main_user = %s",(age_to,user_id))
        db_connect.commit()
        db_connect.close()

        write_msg(user_id = user_id,
                      message = "Конечный возраст изменен!")
        
        return True
    
    except Error as error:
        # Сообщение в логи
        print(f"""{datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')}: Произошла ошибка обновления таблицы!
Текст ошибки: {error.pgerror}
Код ошбики: {error.pgcode}""")

        # Сообщение пользователю 
        write_msg(user_id = user_id,
                      message = "Вовремя изменения произошла ошибка")
        
        db_connect.close()
        return False
    
def update_leave_in_Favorite_list(user_id,find_id) -> bool:
    """
    Функция убирает пользователя из базы белого списка. Однако, не убирает из просмотренных!
    :::ВХОДНЫЕ ДАННЫЕ\n
    user_id -> главный пользователь\n
    find_id -> поисковой пользователь\n
    :::ВЫХОДНЫЕ ДАННЫЕ\n
    True если удалил
    False если не удалил
    """

    db_connect = create_connect()
    cursor = db_connect.cursor()
    
    try:
        cursor.execute("UPDATE users SET likes = 0 WHERE main_user = %s and find_user = %s",(user_id,find_id))
        db_connect.commit()
        db_connect.close()

        write_msg(user_id = user_id,
                      message = "Лайк убран! Идем дальше...")
        
        return True
    
    except Error as error:
        # Сообщение в логи
        print(f"""{datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')}: Произошла ошибка обновления таблицы!
Текст ошибки: {error.pgerror}
Код ошбики: {error.pgcode}""")

        # Сообщение пользователю 
        write_msg(user_id = user_id,
                      message = "Вовремя удаления произошла ошибка, дизлайк не убран!")
        
        db_connect.close()
        return False