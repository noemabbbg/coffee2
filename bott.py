from ast import Call
import asyncio
import logging
import random
import manhwaclass
import aiogram_broadcaster
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.emoji import emojize
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
from aiogram.types import Message, CallbackQuery
from config import TOKEN, MY_ID, channel_id, QIWI_TOKEN
import keyboardkiwi
import keyboardmainmenu
import keyboardmanhwasetup
from keyboardmainmenu import clava, clavaChangeState, nextchapter, checkSubm, cancelsub, returN
from keyboardkiwi import topup, buy_menu, confirmkb
from keyboardmanhwasetup import clavaTOP
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from manhwaclass import stateManhwa, is_number
import dictant
from dictant import Maindict

import os
from mysql.connector import MySQLConnection
from aiogram_broadcaster import TextBroadcaster
from aiogram_broadcaster import MessageBroadcaster
from aiogram.dispatcher import FSMContext
from db import Database, get
from pyqiwip2p import QiwiP2P
from pathlib import Path

#if get.get_user_num(1)>1095:
#    basa='testdatabase2.db'
#else:
basa='testdatabase1.db'
db=Database(basa)
S=stateManhwa()
storage=MemoryStorage()
p2p=QiwiP2P(auth_key=QIWI_TOKEN)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)
def check_sub_channel(chat_member):
    if chat_member['status']!='left':
        return True
    else:
        return False
#####блок рассылки#####
async def subchanneldone(message: types.Message):
    await bot.send_message('133886300', text="broadcast1337 sheesh")
@dp.message_handler(commands=['sheesh'])
async def subchanneldone(message: types.Message):
    await bot.send_message('133886300', text=get.get_user_num(1))
   

@dp.message_handler(commands=['broadcast1337'])
async def broadcast_command_handler(msg: Message, state: FSMContext):
    await msg.answer('Введите текст для начала рассылки:')
    await state.set_state('broadcast_text1')
async def start_broadcast(msg: Message, state: FSMContext):
   
    await state.finish()
    storage = state.storage 
    #users=get.get_user(k)
    await MessageBroadcaster((get.get_user(1)), msg).run()
dp.register_message_handler(broadcast_command_handler, commands='broadcast1337')
dp.register_message_handler(start_broadcast, state='broadcast_text1', content_types=types.ContentTypes.ANY)


async def broadcast_command_handler(msg: Message, state: FSMContext):
    await msg.answer('Введите текст для начала рассылки:')
    await state.set_state('broadcast_text5')
async def start_broadcast(msg: Message, state: FSMContext):
    k=5
    await state.finish()
    storage = state.storage 
    users=get.get_user(k)
    await MessageBroadcaster((get.get_user(5)), msg).run()
dp.register_message_handler(broadcast_command_handler, commands='broadcastsuicideboy')
dp.register_message_handler(start_broadcast, state='broadcast_text5', content_types=types.ContentTypes.ANY)



#####блок рассылки#####

#####блок баланса, пополнения#####
@dp.message_handler(commands=['balance'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, f"СЧЕТ: {db.user_money(message.from_user.id)} руб.", reply_markup=topup)
@dp.callback_query_handler(text_contains="popolnit")
async def process_video_command(call: CallbackQuery): 
    
    message_money=100
    comment=str(call.message.from_user.id) +"_"+ str(random.randint(1000,9999))
    bill=p2p.bill(amount=message_money, lifetime=15, comment=comment)
    db.add_check(call.message.from_user.id, message_money,bill.bill_id)
    await bot.send_message(call.from_user.id, "пополнение на месячную подписку будет 100 рублей",  reply_markup=buy_menu(url=bill.pay_url, bill=bill.bill_id))
       
@dp.callback_query_handler(text="subscribemanagment")
async def chet(call: CallbackQuery):
    if db.state_subscribe(call.from_user.id)==1:
        await bot.send_message(call.from_user.id, text="у вас уже есть подписка и она дейсвтует до:")
    else:
        await bot.send_message(call.from_user.id, f"сейчас на твоем балансе: {db.user_money(call.from_user.id)} руб.")
        await bot.send_message(call.from_user.id, "подписка дает доступ к самым последним главам таких манхв как:  чтобы ее купить нужно пополнить счет на 100рублей и купить по кнопке :)", reply_markup=topup)
@dp.callback_query_handler(text_contains="check_")
async def process_video_command(call: CallbackQuery):
    bill=str(call.data[6:])
    info=db.get_check(bill)
    print(info)
    if info!=False:
        if str(p2p.check(bill_id=bill).status)== "PAID":
            user_money=db.user_money(call.from_user.id)
            money=int(info[2])
            print(money)
            db.set_money(call.from_user.id, user_money+money)
            await bot.send_message(call.from_user.id, f"ваш счет пополнен на: {money} и теперь он составляет: {user_money}")
        else:
            await bot.send_message(call.from_user.id,text="счет не оплачен чел ало", reply_markup=buy_menu(False,bill=bill))
    else:
        await bot.send_message(call.from_user.id,text="счет не найден")


@dp.callback_query_handler(text="subscribeALL")
async def process_video_command(call: CallbackQuery):
    await bot.send_message(call.from_user.id,text="подписка стоит 100рублей, с баланса спишется 100. Подтверждаем?",reply_markup=confirmkb)

@dp.callback_query_handler(text="confirmpay")   
async def da(message:types.Message):
        if (db.user_money(message.from_user.id)==100 or db.user_money(message.from_user.id)>100):
            newmoney=db.user_money(message.from_user.id)-100
            db.pay_subcribe(message.from_user.id, newmoney)
            subscribe=1
            await bot.send_message(message.from_user.id, text="поздравляю, вы приобрели подписку на месяц")
            print(db.state_subscribe(message.from_user.id))
            db.add_subscribe(message.from_user.id, subscribe)
            print(db.add_subscribe(message.from_user.id, subscribe))
        else:
            await bot.send_message(message.from_user.id, text="мало денег чел", reply_markup=topup)

#####блок баланса, пополнения#####

#####блок старта и основного функционала#####
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    #await bot.send_message('133886300', Herokiller)
    if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=message.from_user.id)):
        if not (db.user_exists(message.from_user.id)):
            db.add_user(message.from_user.id)
            await bot.send_message(message.from_user.id, text="привет! сейчас бот работает в тестовом режиме и я буду очень рад, если ты напишешь мне обратную свзяь по работе бота, спасибо! @bububucheel",reply_markup=clava)
        
        else:
            await bot.send_message(message.from_user.id, text="привет! сейчас бот работает в тестовом режиме и я буду очень рад, если ты напишешь мне обратную свзяь по работе бота, спасибо! @bububucheel",reply_markup=clava)
            #await bot.send_video(message.from_user.id, 'BAACAgIAAxkBAAEOfvxiJLqDCnKOI25Av2GcweBAoliyrgACXRYAAtZKKUkAATpjYv3HwMkjBA')
            if not (db.user_exists(message.from_user.id)):
                db.add_user(message.from_user.id)
    else:
         await bot.send_message(message.from_user.id, 'Для работы бота подпишись пожалуйста на канал со всеми новостями и обновлениями, спасибо!', reply_markup=checkSubm)
         if not (db.user_exists(message.from_user.id)):
            db.add_user(message.from_user.id)

@dp.callback_query_handler(text_contains="returnMenu")
async def process_video_command(call: CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer(text="буду рад обратной связи :) @bububucheel",reply_markup=clava)
    buffer=0
    db.addbuffer(call.from_user.id, buffer)
    db.addsearch(call.from_user.id, buffer)

@dp.callback_query_handler(text_contains="subscribeNew")    # подписка на выход новых глав чего-либо (реализовать в одном модуле)
async def broad(call:CallbackQuery):
    if db.statebuffer(call.from_user.id)==6:
        if db.state_broadcast_boxer(call.from_user.id)==0:
            boxerbroadcast=call.from_user.id
            db.add_user_broadcast_boxer(call.from_user.id, boxerbroadcast)
        else: 
            await call.message.answer("кажется ты уже подписан на выход этой манхвы, хочешь отменить?",reply_markup=cancelsub) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("Мы пришлем тебе новую главу как только она выйдет! :)",reply_markup=cancelsub)
    elif db.statebuffer(call.from_user.id)==5:
        if db.state_broadcast_suicideboy(call.from_user.id)==0:
            suicideBoy=call.from_user.id
            db.add_user_broadcast_suicideboy(call.from_user.id, suicideBoy)
        else: 
            await call.message.answer("кажется ты уже подписан на выход этой манхвы, хочешь отменить?",reply_markup=cancelsub) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("Мы пришлем тебе новую главу как только она выйдет! :)",reply_markup=cancelsub)
    elif db.statebuffer(call.from_user.id)==7:
        if db.state_broadcast_suicideboy(call.from_user.id)==0:
            bastard=call.from_user.id
            db.add_user_broadcast_suicideboy(call.from_user.id, bastard)
        else: 
            await call.message.answer("кажется ты уже подписан на выход этой манхвы, хочешь отменить?", reply_markup=cancelsub) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("Мы пришлем тебе новую главу как только она выйдет! :)",reply_markup=cancelsub)
    elif db.statebuffer(call.from_user.id)==8:
        if db.state_broadcast_antifanatka(call.from_user.id)==0:
            bastard=call.from_user.id
            db.add_user_broadcast_antifanatka(call.from_user.id, bastard)
        else: 
            await call.message.answer("кажется ты уже подписан на выход этой манхвы, хочешь отменить?", reply_markup=cancelsub) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("Мы пришлем тебе новую главу как только она выйдет! :)",reply_markup=cancelsub)
    elif db.statebuffer(call.from_user.id)==9:
        if db.state_broadcast_queenwithscalpel(call.from_user.id)==0:
            bastard=call.from_user.id
            db.add_user_broadcast_queenwithscalpel(call.from_user.id, bastard)
        else: 
            await call.message.answer("кажется ты уже подписан на выход этой манхвы, хочешь отменить?", reply_markup=cancelsub) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("Мы пришлем тебе новую главу как только она выйдет! :)",reply_markup=cancelsub)
    elif db.statebuffer(call.from_user.id)==10:
        if db.state_broadcast_odnazhprinc(call.from_user.id)==0:
            bastard=call.from_user.id
            db.add_user_broadcast_odnazhprinc(call.from_user.id, bastard)
        else: 
            await call.message.answer("кажется ты уже подписан на выход этой манхвы, хочешь отменить?", reply_markup=cancelsub) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("Мы пришлем тебе новую главу как только она выйдет! :)",reply_markup=cancelsub)
    elif db.statebuffer(call.from_user.id)==11:
        if db.state_broadcast_chertovka(call.from_user.id)==0:
            bastard=call.from_user.id
            db.add_user_broadcast_chertovka(call.from_user.id, bastard)
        else: 
            await call.message.answer("кажется ты уже подписан на выход этой манхвы, хочешь отменить?", reply_markup=cancelsub) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("Мы пришлем тебе новую главу как только она выйдет! :)",reply_markup=cancelsub)






@dp.callback_query_handler(text_contains="cancelmanhwasub")
async def cancelsubfunc(call:CallbackQuery):
    if db.statebuffer(call.from_user.id)==6:
        if db.state_broadcast_boxer(call.from_user.id)==call.from_user.id:
            boxerbroadcast=0
            db.add_user_broadcast_boxer(call.from_user.id, boxerbroadcast)
        else: 
            await call.message.answer("отменили твою подписку!",reply_markup=returN) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("твоя подписка  отменена")
    elif db.statebuffer(call.from_user.id)==5:
        if db.state_broadcast_suicideboy(call.from_user.id)==call.from_user.id:
            suicideBoy=0
            db.add_user_broadcast_suicideboy(call.from_user.id, suicideBoy)
        else: 
            await call.message.answer("отменили твою подписку!",reply_markup=returN) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("твоя подписка отменена")
    elif db.statebuffer(call.from_user.id)==7:
        if db.state_broadcast_suicideboy(call.from_user.id)==call.from_user.id:
            bastard=0
            db.add_user_broadcast_suicideboy(call.from_user.id, bastard)
        else: 
            await call.message.answer("отменили твою подписку!", reply_markup=returN) #в этом блоке нужно дописаь и реализовать функционал отмены рассылки
        await call.message.answer("твоя подписка отменена")



@dp.callback_query_handler(text_contains="саб")
async def subfunc(call:CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=call.from_user.id)):
        await call.message.answer(text="привет! сейчас бот работает в тестовом режиме и я буду очень рад, если ты напишешь мне обратную свзяь по работе бота, спасибо! @bububucheel", reply_markup=clava)
    else:
        await call.bot.send_message(call.from_user.id, 'Для просмотра сначала подпишись на канал', reply_markup=checkSubm)

@dp.callback_query_handler(text_contains="топ")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('🤔 что же выбрать', reply_markup=keyboardmanhwasetup.clavaViborGenre)

@dp.callback_query_handler(text_contains="Romantik")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('🤔 что же выбрать', reply_markup=keyboardmanhwasetup.Clavaromantik)


@dp.callback_query_handler(text_contains="Ekhn")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('🤔 что же выбрать', reply_markup=keyboardmanhwasetup.ClavaEkhn)


@dp.callback_query_handler(text_contains="Triller")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('🤔 что же выбрать', reply_markup=keyboardmanhwasetup.clavaTriller)

@dp.callback_query_handler(text_contains="Cultivation")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('🤔 что же выбрать', reply_markup=keyboardmanhwasetup.ClavaCultivation)

@dp.callback_query_handler(text_contains="Isekai")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('🤔 что же выбрать', reply_markup=keyboardmanhwasetup.ClavaIsekai)


@dp.callback_query_handler(text_contains="Drama")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('🤔 что же выбрать', reply_markup=keyboardmanhwasetup.ClavaDrama)



@dp.callback_query_handler(text_contains="Back")
async def process_video_command(call: CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer(text="буду рад обратной связи :) @bububucheel",reply_markup=keyboardmanhwasetup.clavaViborGenre)
    buffer=0
    db.addbuffer(call.from_user.id, buffer)
    db.addsearch(call.from_user.id, buffer)

@dp.callback_query_handler(text_contains="поиск главы")
async def process_video_command(call: CallbackQuery):
    buffer=db.statebuffer(call.from_user.id) 
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    await call.message.answer('доступные главы:')
    
    
    list_keys = list(Maindict[buffer].keys())
    list_keys.sort()
    await bot.send_message(call.from_user.id, text=(list_keys))
    await call.message.answer('введи номер главы с которой ты хочешь продолжить читать')
    @dp.message_handler()
    async def buffer(message: types.Message):
            buff=int(message.text)
            db.addsearch(message.from_user.id, buff)
            search=db.statesearch(message.from_user.id)
            buffer=db.statebuffer(message.from_user.id)
            user_id = message.from_user.id
            slovo=Maindict[buffer][search]
            if buff==S.payfullChapters[buffer]:
                   if db.state_subscribe(message.from_user.id)==1:
                        try:
                            await bot.send_message(message.from_user.id, text='глава по подписке')
                            await bot.send_video(message.from_user.id, video=slovo, reply_markup=nextchapter)
                        except:
                            await bot.send_message(message.from_user.id, text='кажется этой главы еще нет :(', reply_markup=clavaTOP)
                   else:
                        await bot.send_message(message.from_user.id, text='эта глава доступна по подписке')
            else:
                try:
                    await bot.send_video(message.from_user.id, video=slovo, reply_markup=nextchapter)
                except:
                    await bot.send_message(message.from_user.id, text='кажется этой главы еще нет :(', reply_markup=clavaTOP)



@dp.callback_query_handler(text_contains="начать с начала")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    buffer=db.statebuffer(call.from_user.id)
    await call.message.answer('чтение с нулевой главы')
    await call.bot.send_video(call.from_user.id, video=Maindict[buffer][1], reply_markup=nextchapter)

@dp.callback_query_handler(text_contains="next")
async def nextSERIA(message:types.Message): 
    buffer=db.statebuffer(message.from_user.id)
    search1=db.statesearch(message.from_user.id)+1
    db.addsearch(message.from_user.id, search1)
    search=db.statesearch(message.from_user.id)
    try:
        await bot.send_video(message.from_user.id, Maindict[buffer][search], reply_markup=nextchapter) 
    except:
         await bot.send_message(message.from_user.id, text="кажется эта глава еще не добавлена :(,\n попробуй что нибудь другое", reply_markup=clavaTOP)


@dp.callback_query_handler(text_contains="download")
async def process_video_command(call: CallbackQuery):
    buffer=db.statebuffer(call.from_user.id)
    list_keys = list(Maindict[buffer].keys())
    k=len(list_keys)
    await bot.send_message(call.from_user.id, text="высылаю все главы этой манхвы, wait... если что-то пошло не так - пиши /start")
    if (buffer==16):
        for i in range(140,206):
            await asyncio.sleep(0.2)
            await bot.send_video(call.from_user.id, Maindict[buffer][i])
    else:
        for i in range(1,k):
            await asyncio.sleep(0.2)
            await bot.send_video(call.from_user.id, Maindict[buffer][i])
    await bot.send_message(call.from_user.id, text="Хорошего чтения", reply_markup=returN)




@dp.callback_query_handler(text_contains="KRD")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=call.from_user.id)):
        await bot.delete_message(call.from_user.id, call.message.message_id)
        #await bot.send_photo(call.from_user.id, caption='*Описание:* \n animeeeeee"*', photo="AgACAgIAAxkDAAIhVWINR-aKU3-Tz-yo8dyvgNeYy1u9AAJVvDEbkSBoSNxtsPC6YGn7AQADAgADeAADIwQ", reply_markup=clavaChangeState, parse_mode="Markdown")
        await call.message.answer(text='*Описание:* \n anumeeee', reply_markup=clavaChangeState, parse_mode="Markdown")
        
    else:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await call.bot.send_message(call.from_user.id, 'Для просмотра сначала подпишись на канал', reply_markup=checkSubm)
    buffer=1
    db.addbuffer(call.from_user.id, buffer)


@dp.callback_query_handler(text_contains="Pharh")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=call.from_user.id)):
        await bot.delete_message(call.from_user.id, call.message.message_id)
        #await bot.send_photo(call.from_user.id, caption='*Описание:* \n animeeeeee"*', photo="AgACAgIAAxkDAAIhVWINR-aKU3-Tz-yo8dyvgNeYy1u9AAJVvDEbkSBoSNxtsPC6YGn7AQADAgADeAADIwQ", reply_markup=clavaChangeState, parse_mode="Markdown")
        await call.message.answer(text='*Описание:* \n anumeeee', reply_markup=clavaChangeState, parse_mode="Markdown")
        
    else:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await call.bot.send_message(call.from_user.id, 'Для просмотра сначала подпишись на канал', reply_markup=checkSubm)
    buffer=2
    db.addbuffer(call.from_user.id, buffer)


@dp.callback_query_handler(text_contains="Zugumomo")
async def process_video_command(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"callback_data='{callback_data}'")
    if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=call.from_user.id)):
        await bot.delete_message(call.from_user.id, call.message.message_id)
        #await bot.send_photo(call.from_user.id, caption='*Описание:* \n animeeeeee"*', photo="AgACAgIAAxkDAAIhVWINR-aKU3-Tz-yo8dyvgNeYy1u9AAJVvDEbkSBoSNxtsPC6YGn7AQADAgADeAADIwQ", reply_markup=clavaChangeState, parse_mode="Markdown")
        await call.message.answer(text='*Описание:* \n anumeeee', reply_markup=clavaChangeState, parse_mode="Markdown")
        
    else:
        await bot.delete_message(call.from_user.id, call.message.message_id)
        await call.bot.send_message(call.from_user.id, 'Для просмотра сначала подпишись на канал', reply_markup=checkSubm)
    buffer=3
    db.addbuffer(call.from_user.id, buffer)
##### требует конкретной записи, но куда и как?????




#####блок старта и основного функционала#####




#####блок callbackov манхв#####


























if __name__ == '__main__':
    executor.start_polling(dp)






