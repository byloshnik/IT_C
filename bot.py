import sqlite3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton

bot = Bot(token='1851793811:AAHkSAyxTC8q00qBbGa78c8uNJgvoyrIsws')
dp = Dispatcher(bot)
'''1111'''
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nЯ твой первый бот для IT-Fest!")
    connect = sqlite3.connect('db_students.db')
    cursor = connect.cursor()
    connect.commit()

    user_id = message.chat.id
    user_name = message.chat.username
    cursor.execute(f'SELECT id FROM Students WHERE id = {user_id}')
    data = cursor.fetchone()
    connect.commit()
    print(data)
    print(user_id, user_name)

    if data is None:
        cursor.execute("INSERT INTO Students VALUES(?,?,?);", (user_id,user_name, 0))
        connect.commit()
    else: print("Такой пользователь уже существует")

@dp.message_handler(commands=['deleteme'])
async def process_help_command(message: types.Message):
    connect = sqlite3.connect('db_students.db')
    cursor = connect.cursor()
    user_id = message.chat.id
    cursor.execute(f'DELETE FROM Students WHERE id = {user_id}')
    connect.commit()

@dp.message_handler(text = 'Поднять рейтинг')
async def process_help_command(message: types.Message):
    connect = sqlite3.connect('db_students.db')
    cursor = connect.cursor()
    user_id = message.chat.id
    cursor.execute(f'SELECT rate FROM Students WHERE id = {user_id}')
    r1 = cursor.fetchone()
    print(r1)
    cursor.execute(f'UPDATE Students SET rate= {r1[0]+1} WHERE id ={user_id}')
    connect.commit()

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и повторю за тобой, как эхо!")

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)

if __name__ == '__main__':
    executor.start_polling(dp)


