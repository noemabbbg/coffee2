from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from dictant import Zugumomo
btnreturnmenu=InlineKeyboardButton(text='вернуться в меню↩️', callback_data='returnMenu')



clavaTOP = InlineKeyboardMarkup(row_width=1)




back=InlineKeyboardButton(text="вернуться↩️", callback_data="Back")
#clavaTOP.insert(GreenLight)
clavaTOP.insert(btnreturnmenu)

####28


clavaViborGenre=InlineKeyboardMarkup(row_width=1)
buy_pear1 = InlineKeyboardButton(text="Романтика", callback_data="Romantik")
buy_pear2 = InlineKeyboardButton(text="Экшн", callback_data="Ekhn")
buy_pear3 = InlineKeyboardButton(text="Триллер", callback_data="Triller")

buy_pear5 = InlineKeyboardButton(text="Драма", callback_data="Drama")
buy_pear6 = InlineKeyboardButton(text="Исекай", callback_data="Isekai")

clavaViborGenre.insert(buy_pear1)
clavaViborGenre.insert(buy_pear2)
#clavaViborGenre.insert(buy_pear3)

#clavaViborGenre.insert(buy_pear5)
#clavaViborGenre.insert(buy_pear6)
clavaViborGenre.insert(btnreturnmenu)

ClavaDrama=InlineKeyboardMarkup(row_width=1)

ClavaDrama.insert(back)


Clavaromantik=InlineKeyboardMarkup(row_width=1)
Pharh=InlineKeyboardButton(text='Эта фарфоровая кукла влюбилась', callback_data='Pharh')
Zugumomo=InlineKeyboardButton(text='Цугумомо', callback_data='Zugumomo')
Clavaromantik.insert(Pharh)
Clavaromantik.insert(Zugumomo)
Clavaromantik.insert(back)  



ClavaEkhn=InlineKeyboardMarkup(row_width=1)
KRD=InlineKeyboardButton(text='Клинок, рассекающий демонов (1)', callback_data='KRD')
ClavaEkhn.insert(KRD)
ClavaEkhn.insert(Zugumomo)
ClavaEkhn.insert(back)





clavaTriller=InlineKeyboardMarkup(row_width=1)
     
clavaTriller.insert(back)


ClavaIsekai=InlineKeyboardMarkup(row_width=1)

ClavaIsekai.insert(back)





ClavaCultivation=InlineKeyboardMarkup(row_width=1)
    
ClavaCultivation.insert(btnreturnmenu)




