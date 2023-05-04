import vk_api
import pandas as pd

from config.config import (access_token_group,
                           vk_access_token,
                           version_api,
                           group_id)

from random import randrange


import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError


from pprint import pprint
