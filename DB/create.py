
def create_table_users(connection):
    value = """CREATE TABLE IF NOT EXISTS users (
                bd_id serial PRIMARY KEY,
                age int,
                interests text,
                online_app int,
                online_mobile int,
                id INTEGER NULL,
                track_code text,
                maiden_name text,
                nickname text,
                domain text,
                bdate text,
                city_id int,
                city_title text,
                has_photo int,
                home_town text,
                sex int,
                friend_status int,
                first_name text,
                last_name text,
                online int,
                screen_name text,
                verified int,
                can_access_closed boolean,
                is_closed boolean,
                link_pro text,
                photo_1_url text,
                photo_1_id int,
                photo_1_likes int,
                photo_2_url text,
                photo_2_id int,
                photo_2_likes int,
                photo_3_url text,
                photo_3_id int,
                photo_3_likes int

             );"""
    connection.execute(value)


def create_table_search_params(connection):
    value = """CREATE TABLE IF NOT EXISTS search_params (
                bd_id serial PRIMARY KEY,
                param_sex INTEGER NULL,
                param_city INTEGER NULL,
                param_age_from INTEGER NULL,
                param_age_to INTEGER NULL,
                param_status INTEGER NULL,
                id_user integer null,
                FOREIGN KEY (id_user) REFERENCES users (bd_id) ON DELETE CASCADE
             );"""
    connection.execute(value)


def create_table_favorites_users(connection):
    value = """CREATE TABLE IF NOT EXISTS favorites_users (
                 fav_user_id integer references users(bd_id),
                 id_user integer references users(bd_id),
                 constraint favorites_users_id primary key (fav_user_id, id_user)
             );"""
    connection.execute(value)


def create_table_black_list(connection):
    value = """CREATE TABLE IF NOT EXISTS black_list (
                 bl_list_id integer references users(bd_id),
                 id_user integer references users(bd_id),
                 constraint black_list_id primary key (bl_list_id, id_user)
             );"""
    connection.execute(value)


def create_all_tables(connection):
    create_table_users(connection)
    create_table_search_params(connection)
    create_table_favorites_users(connection)
    create_table_black_list(connection)


def creat_all_tables(connection):
    conn = connection
    create_all_tables(conn)
    conn.close()
