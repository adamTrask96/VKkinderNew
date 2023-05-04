from DB.select import select_nalichie_users_DB

import datetime


def add_users(connection, users_dict):
    for key in users_dict.keys():
        data = select_nalichie_users_DB(connection, key)
        if data == []:
            value = '''insert into users('''
            columns = ''''''
            values = ''''''
            for key2 in users_dict[key].keys():
                if type(users_dict[key][key2]) == str:
                    if "'" in users_dict[key][key2]:
                        users_dict[key][key2] = users_dict[key][key2].replace("'",'"')
                columns += f'''"{key2}",'''
                values += f"""'{users_dict[key][key2]}',"""
            columns = columns[:-1]
            values = values[:-1]
            
            value = value + columns + ') values (' + values + ');'
            connection.execute(value)
            print('Пользователь добавлен в БД')
        else:
            print('Пользователь уже есть в БД')
    return 

def add_users_and_search_params(connection, users_dict, sex, age_from, age_to, city, status):
    for key in users_dict.keys():
        data = select_nalichie_users_DB(connection, key)
        if data == []:
            value = '''insert into users('''
            columns = ''''''
            values = ''''''
            for key2 in users_dict[key].keys():
                if type(users_dict[key][key2]) == str:
                    if "'" in users_dict[key][key2]:
                        users_dict[key][key2] = users_dict[key][key2].replace("'",'"')
                columns += f'''"{key2}",'''
                values += f"""'{users_dict[key][key2]}',"""
            columns = columns[:-1]
            values = values[:-1]
            value = value + columns + ') values (' + values + ') RETURNING bd_id;'
            n = connection.execute(value).fetchone()
            add_search_params(connection, n[0], sex, age_from, age_to, city, status, key)
            print('Пользователь добавлен в БД')
        else:
            print('Пользователь уже есть в БД')

def add_search_params(connection, bd_id, sex, age_from, age_to, city, status,key):
    connection.execute("""INSERT INTO search_params(param_sex, param_age_from, param_age_to, param_city, param_status, bd_id, id_user)
                VALUES (%s,%s,%s,%s,%s,%s,%s)""",(str(sex),str(age_from),str(age_to),str(city),str(status),str(bd_id),str(bd_id)))
    print('Параметры поиска добавлены в БД')

def add_favorites_users(connection, user_id, id_in_list):
    try:
        value = f"INSERT INTO favorites_users (id_user, fav_user_id) VALUES ({user_id}, {id_in_list});"
        connection.execute(value)
        print('Пользователь добавлен в Избранное')
        return
    except:
        return "Пользователь уже есть в избранном"

def add_black_list(connection, user_id, id_in_list):
    try:
        value = f"INSERT INTO black_list (id_user, bl_list_id) VALUES ({user_id}, {id_in_list});"
        connection.execute(value)
        print('Пользователь добавлен в черный список')
        return
    except:
        return "Пользователь уже есть в черном списке"
