import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll


class VKConnect:
    _bot_token = os.getenv('VKINDER_API_KEY')

    user_session = VkApi(token=os.getenv('VK_API_KEY'))
    bot_session = VkApi(token=_bot_token)
    longpoll = VkLongPoll(bot_session)


class BDConnect:
    _db = f'postgresql://{os.getenv("BD_USER")}:{os.getenv("BD_PWD")}@localhost:5432/vkinder'

    engine = create_engine(_db)
    session = sessionmaker(bind=engine)()
