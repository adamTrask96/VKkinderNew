from DB.connect import create_connect # DB.connect
from psycopg2 import Error
import datetime
from functions import write_msg
from app.users import users_get
"""
ЛОГИКА ФАЙЛА!!
Файл необходим для добавления таких данных как:
1) Новый юзер (добавляются его id, и параметры поиска)
2) Добавление(обнавление данных для фавариторв)
3) Добавление (обновление данных для блока)
4) Добавление просмотренных пользователей (чтобы система не повторяла их)
"""

# Добавление нового пользователя и его параметров
def insert_new_user_and_insert_params(user_id, text:str) -> bool:
    """
    Функция необходима для создания нового пользователя и внесения его параметров в базу\n
    :::ВХОДНЫЕ ПАРАМЕТРЫ\n
    cursor -> функциональное обращение к БД\n
    text -> Текст регистрации нового пользователя\n
        Формат текста: \n
        -----------------------\n
        Возраст от: 29\n
        Возраст до: 36\n
        Пол: М\n
        Семейное положение: 1\n
        -----------------------\n
    :::ВЫХОДНЫЕ ДАННЫЕ\n
    Добавлен новый пользователь с параметрами
    """

    try:
        params = {}
        new_text = text.replace('возраст от:','').strip()
        text = new_text.replace('возраст до:','').strip()
        new_text = text.replace('пол:','').strip()
        text = new_text.replace('семейное положение:','').strip()
        text = text.split("\n")
        user_info = users_get(user_id)

        if 0 > int(text[0].strip()) or int(text[0].strip()) > 100:
            raise ValueError("Введено не верное начальное значение возроста! \nПовторите попытку")       
        elif 0 > int(text[1].strip()) or int(text[0].strip()) > 100:
            raise ValueError("Введено не верное конечное значение возроста! \nПовторите попытку")  
        elif text[2].strip() not in ['1','2']:
            raise ValueError("Введено не верное значение пола! \nПовторите попытку")        
        elif 8 < int(text[3].strip()) or int(text[3].strip()) < 0:
            raise ValueError("Введено не верное значение семейного положения! \nПовторите попытку")
        
        params["Возрост от"] = int(text[0].strip())
        params["Возрост до"] = int(text[1].strip())
        params["Пол"] = int(text[2].strip())
        params["Семейное положение"] = int(text[3].strip())
        
        db_connect = create_connect()
        cursor = db_connect.cursor()

        try:
            cursor.execute("INSERT INTO find_params VALUES(%s,%s,%s,%s,%s,%s)",
                       (user_id,params["Пол"],params["Возрост от"],params["Возрост до"],'110',params["Семейное положение"]))
            db_connect.commit()
            db_connect.close()
            return True

        except Error as error:
            # Сообщение  в логи
            print(f"""{datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')}: Произошла ошибка добавления нового пользователя!
Текст ошибки: {error.pgerror}
Код ошбики: {error.pgcode}""")
            
            # Сообщение пользователю
            write_msg(user_id = user_id,
                      message = "Вовремя добавления произошла ошибка, пожалуйста повторите попытку позднее!")
            
            db_connect.close()
            return False
        
    except ValueError as error:
        # Сообщение пользователю
        write_msg(user_id = user_id,
                  message = error.args)
        return False 

# Добавление лайков
def insert_favorite_user(main_user = 1111,find_user = 11102) -> bool:
    """
    Функция реализует лайки пользователю ( в дальнейшем, человек сможет их просматривать)\n
    :::ВХОДНЫЕ ДАННЫЕ\n
    main_user -> id главного пользователя\n
    find_user -> id поискового юзера\n
    :::ВЫХОДНЫЕ ДАННЫЕ\n
    Добавление лайка пользователю 
    """

    db_connect = create_connect()
    cursor = db_connect.cursor()

    try:
        cursor.execute("INSERT INTO users VALUES(%s,%s,1)",(main_user,find_user))
        db_connect.commit()
        db_connect.close()

        write_msg(user_id = main_user,
                      message = "Лайк поставлен! Идем дальше...")
        
        return True
    
    except Error as error:
        # Сообщение в логи
        print(f"""{datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')}: Произошла ошибка добавления нового пользователя!
Текст ошибки: {error.pgerror}
Код ошбики: {error.pgcode}""")

        # Сообщение пользователю 
        write_msg(user_id = main_user,
                      message = "Вовремя добавления произошла ошибка, лайк не поставлен!")
        
        db_connect.close()
        return False

# Добавление дизлайков
def insert_Dislike_user(main_user = 1111,find_user = 11102) -> bool:
    """
    Функция реализует лайки пользователю ( в дальнейшем, человек сможет их просматривать)\n
    :::ВХОДНЫЕ ДАННЫЕ\n
    main_user -> id главного пользователя\n
    find_user -> id поискового юзера\n
    :::ВЫХОДНЫЕ ДАННЫЕ\n
    Добавление лайка пользователю 
    """

    db_connect = create_connect()
    cursor = db_connect.cursor()
    
    try:
        cursor.execute("INSERT INTO users VALUES(%s,%s,2)",(main_user,find_user))
        db_connect.commit()
        db_connect.close()

        write_msg(user_id = main_user,
                      message = "ДизЛайк поставлен! Идем дальше...")
        
        return True
    
    except Error as error:
        # Сообщение в логи
        print(f"""{datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')}: Произошла ошибка добавления нового пользователя!
Текст ошибки: {error.pgerror}
Код ошбики: {error.pgcode}""")

        # Сообщение пользователю 
        write_msg(user_id = main_user,
                      message = "Вовремя добавления произошла ошибка, дизлайк не поставлен!")
        
        db_connect.close()
        return False
    
# Простой просмотре пользователей
def insert_watched_user(main_user = 1111,find_user = 11102) -> bool:
    """
    Функция реализует добавление просмотренного пользователя\n
    :::ВХОДНЫЕ ДАННЫЕ\n
    main_user -> id главного пользователя\n
    find_user -> id поискового юзера\n
    :::ВЫХОДНЫЕ ДАННЫЕ\n
    TRUE -> Пользователь успешно был добавлен в систему
    FLASE -> Произошла какая-то ошибка
    """

    db_connect = create_connect()
    cursor = db_connect.cursor()
    
    try:
        cursor.execute("INSERT INTO users VALUES(%s,%s,0)",(main_user,find_user))
        db_connect.commit()
        db_connect.close()
        return True

    except Error as error:
        # Сообщение в логи
        print(f"""{datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')}: Произошла ошибка добавления нового пользователя!
Текст ошибки: {error.pgerror}
Код ошбики: {error.pgcode}""")

        # Сообщение пользователю 
        write_msg(user_id = main_user,
                      message = "Вовремя добавления произошла ошибка, пользователь не был добавлен в просмотренные!")
        
        db_connect.close()
        return True

if __name__ == "__main__":
    insert_new_user_and_insert_params(text="""Возрост от: 5
        Возрос до: 60
        Пол: 1
        Семейное положение: 0""")
    insert_favorite_user()
    insert_Dislike_user()
    insert_watched_user()