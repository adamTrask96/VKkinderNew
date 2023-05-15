from DB.connect import create_connect
from pprint import pprint
"""
ЛОГИКА ФАЙЛА!!!\n

для просмотра данных, нам необходимо такие запросы как:\n
1) запрос на нахождение пользователя в чс(не нравиться)\n
2) запрос на нахождение пользователя в лайках(нравиться)\n
3) запрос параметров поиска от пользователя\n
4) запрос на нахождиение поискового пользователя\n
"""

# Запрос на нахождение пользователя в чс (значение 2)
def select_user_in_black(main_user = 1111) -> list:
    """
    Функция для нахождения пользователя в списках чс\n
    ::ВХОДНЫЕ ДАННЫЕ\n
    main_user -> Главный пользователь\n
    find_user -> Поисковой пользователь\n
    ::ВЫХОДНЫЕ ДАННЫЕ\n
    bool значения. Если пользователь находиться в списках, то возращается True ИНАЧЕ False\n
    """
    
    db_connect = create_connect()
    cursor = db_connect.cursor()
    
    cursor.execute("SELECT find_user FROM users WHERE main_user = %s AND likes = 2",(main_user,))
    number = cursor.fetchall()

    db_connect.close()
    
    return number

# Запрос на нахождение пользователя в лайках (значение 1)
def select_user_in_favorite(main_user = 1111) -> list:
    """
    Функция для нахождения пользователя в списках фаваритов\n
    ::ВХОДНЫЕ ДАННЫЕ\n
    main_user -> Главный пользователь\n
    find_user -> Поисковой пользователь\n
    ::ВЫХОДНЫЕ ДАННЫЕ\n
    bool значения. Если пользователь находиться в списках, то возращается True ИНАЧЕ False\n
    """
    
    db_connect = create_connect()
    cursor = db_connect.cursor()
    
    cursor.execute("SELECT find_user FROM users WHERE main_user = %s AND likes = 1",(main_user,))
    number = cursor.fetchall()

    return number

# Запрос параметров поиска от пользователя
def select_params_of_user(number_id_main_user = 1111) -> list:
    """
    Функция для получения данных, которые нужны во время поиска\n
    ::ВХОДНЫЕ ДАННЫЕ\n
    Пока не известно(сделать на вход, данные пользователя вк)\n
    ::ВЫХОДНЫЕ ДАННЫЕ\n
    Список данных, в формате:\n
        {
        Возрост от: 29,\n
        Возрос до: 30,\n
        Пол: 1,\n
        Город: Пермь/200,\n
        Семейное положение: 1
        }

    """
    
    db_connect = create_connect()
    cursor = db_connect.cursor()

    cursor.execute("SELECT sex, age_from, age_to, city, relation FROM find_params WHERE main_user = %s",
                   (number_id_main_user,))
    number = cursor.fetchone()
    
    db_connect.close()

    if number is None:
        return None
    
    return [number[1],number[2],number[0],number[3],number[4]]

# Запрос на пользователей, которые уже были
def select_find_user_in_DB(main_user = 1111,find_user = 1110) -> bool:
    """
    Функция проверяет наличие поискового пользователя в бд.\n
    Это исключает повторное появление анкеты у одного человека.\n
    :::ВХОДНЫЕ ДАННЫЕ\n
    main_user -> Главный пользователь\n
    find_user -> Поисковой пользователь\n
    :::ВЫХОДНЫЕ ДАННЫЕ\n
    BOOL значение, если находиться пользователь в базе или нет
    """

    db_connect = create_connect()
    cursor = db_connect.cursor()
    
    cursor.execute("SELECT likes FROM users WHERE main_user = %s AND find_user = %s;",
                (main_user,find_user))
    user = cursor.fetchone()
    db_connect.close()
    
    if user is None:
        return False
    
    return True

if __name__ == "__main__":
    print(select_user_in_black())
    print(select_user_in_favorite())
    pprint(select_params_of_user())
    print(select_find_user_in_DB())

"""
# Выбор id в БД по id пользователя vk
def select_nalichie_users_DB(connection, id_vk):
    value = f"SELECT bd_id,id FROM users WHERE id = %s;"
    data = connection.execute(value, (id_vk,)).fetchall()
    return data

# Проверка наличия пользователей в чс
def select_nalichie_in_blacklist(connection,id_vk):
    query = "SELECT * FROM black_list WHERE bl_list_id = %s;"
    data = connection.execute(query, (id_vk,)).fetchone()
    return data

# Проверка наличия пользователя в фаваритах
def select_nalicie_in_favorites(connection,id_vk):
    query = "SELECT * FROM favorites_users WHERE fav_user_id = %s;"
    data = connection.execute(query, (id_vk,)).fetchone()
    return data 

# Проверка наличия в ЧС
def select_blacklist(connection, bd_id):
    value = f"SELECT bl_list_id FROM black_list WHERE id_user = %s;"
    data = connection.execute(value, (bd_id,)).fetchall()
    return data

# Проверка наличия в избранных
def select_favorites(connection, bd_id):
    value = f"SELECT fav_user_id FROM favorites_users WHERE id_user = %s;"
    data = connection.execute(value, (bd_id,)).fetchall()
    return data

# Выбор id БД для просмотра
def select_search_params(connection, sex, age_at, age_to, city, status):
    table1 = 'search_params'
    column1 = 'param_sex'
    column2 = 'param_city'
    column3 = 'param_age_from'
    column4 = 'param_age_to'
    column5 = 'param_status'
    column6 = 'id_user'
    value = f"SELECT {column6} FROM {table1} WHERE {column1} = %s AND {column2} = %s AND {column3} = %s AND {column4} = %s AND {column5} = %s;"
    data = connection.execute(value, (sex, city, age_at, age_to, status)).fetchall()
    users_for_view = {}
    n = 1
    for exec in data:
        black_list = select_nalichie_in_blacklist(connection, exec[0])
        favorites = select_nalicie_in_favorites(connection, exec[0])

        if not black_list and not favorites:
            users_for_view[n] = exec[0]
            n += 1
    return users_for_view  

# Поиск bd_id пользователя
def select_db_id_user(connection,id):
    table = 'users'
    value = f"SELECT bd_id FROM users WHERE id = %s;"
    data = connection.execute(value, (id,)).fetchone()
    return data

# Выборка одного аккаунта для просмотра
def select_one_user_for_view(connection, bd_id):
    table = 'users'
    value = f"SELECT * FROM {table} WHERE bd_id = %s;"
    data = connection.execute(value, (bd_id,)).fetchone()
    data_rezult = {"bd_id":data[0],
                    "age":data[1],
                    "interests":data[2],
                    "online_app":data[3],
                    "online_mobile":data[4],
                    "id":data[5],
                    "track_code":data[6],
                    "maiden_name":data[7],
                    "nickname":data[8],
                    "domain":data[9],
                    "bdate":data[10],
                    "city_id":data[11],
                    "city_title":data[12],
                    "has_photo":data[13],
                    "home_town":data[14],
                    "sex":data[15],
                    "friend_status":data[16],
                    "first_name":data[17],
                    "last_name":data[18],
                    "online":data[19],
                    "screen_name":data[20],
                    "verified":data[21],
                    "can_access_closed":data[22],
                    "is_closed":data[23],
                    "link_pro":data[24],
                    "photo_1_url":data[25],
                    "photo_1_id":data[26],
                    "photo_1_likes":data[27],
                    "photo_2_url":data[28],
                    "photo_2_id":data[29],
                    "photo_2_likes":data[30],
                    "photo_3_url":data[31],
                    "photo_3_id":data[32],
                    "photo_3_likes":data[0]}
    return data_rezult
    """