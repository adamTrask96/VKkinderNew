# from config.config  import (bd_user, bd_password, bd_database) #Основные данные

import psycopg2 as PostgreSQL
from psycopg2 import OperationalError
import datetime

"""
Файл подключения к базе данных.
Обработка коннектов к бд происходит через try->except в связи  с тем, чтобы показать разработчику или человеку,
который будет следить за работой бота, что во время какого-то коннекта произошла ошибка.
"""


def create_connect():
    """
    Функция производит коннект к "локальной" базе данных.\n
    ::ВХОДНЫЕ ДАННЫЕ\n
    Отсутсвуют.\n
    ::ВЫХОДНЫЕ ДАННЫЕ\n
    connect_db -> Готовая, подключенная сессия.\n
    ::ОШИБКИ\n
    Не верно веденные данные подключения к базе данных;\n
    Отсутсвие интернета;\n
    Нет ответа от подключаемой базы данных.\n
    """

    # Данные для проверки
    bd_user = 'postgres'
    bd_password = 'YmkaTheBest'
    bd_database = 'TestBd'

    try:
        connect_db = PostgreSQL.connect(f'postgresql://{bd_user}:{bd_password}@localhost:5432/{bd_database}',
                                        client_encoding='utf8')

        return connect_db

    except OperationalError as error:

        print(f"{datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')}: Произошла ошибка подключения к PostgreSQL, пожалуйста, проверьте данные!",error)


if __name__ == "__main__":
    create_connect()
