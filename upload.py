import os
import asyncio
import logging
from tkinter import EventType
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeVideo
from aiogram import Bot
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from db_map import Base, MediaIds

from config import TOKEN, MY_ID, DB_FILENAME

logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

engine = create_engine(f'sqlite:///{DB_FILENAME}')

if not os.path.isfile(f'./{DB_FILENAME}'):
    Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

bot = Bot(token=TOKEN)


entity = 'AudioTube_bot' 
api_id = 11304076
api_hash = '3b12e5f0c726294395444e1a8c7e3cee'
phone =  '+79998197749'
client = TelegramClient(entity, api_id, api_hash)
client.start(phone=+79998197749)
BASE_MEDIA_PATH = '/Users/f/Desktop/new'


async def uploadMediaFiles(folder, method, file_attr):
    folder_path = os.path.join(BASE_MEDIA_PATH, folder)
    for filename in os.listdir(folder_path):
        if filename.startswith('.'):
            continue

        logging.info(f'Started processing {filename}')
        with open(os.path.join(folder_path, filename), 'rb') as file:
            msg =await method(133886300, file, disable_notification=True)
            file_id=getattr(msg, file_attr).file_id
            session = Session()
            newItem = MediaIds(file_id=file_id, filename=filename)
            try:
                session.add(newItem)
                session.commit()
                f=open('file.txt', 'a')
            except Exception as e:
                logging.error(
                    'Couldn\'t upload {}. Error is {}'.format(filename, e))
            else:

                f.write(filename+": '"+ file_id + "', " + "\n")
            finally:
                session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(uploadMediaFiles('videos', client.send_file, 'video'))
