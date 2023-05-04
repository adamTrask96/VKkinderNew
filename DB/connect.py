from config.config  import (bd_user, bd_password, bd_database)

import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker



def create_connect():
    engine = sq.create_engine(f'postgresql://{bd_user}:{bd_password}@localhost:5432/{bd_database}',
                            client_encoding='utf8')



    Session = sessionmaker(bind=engine)
    session = Session()
    connection = engine.connect()
    return connection

