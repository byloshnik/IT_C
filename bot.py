import sqlite3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup,KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton, CallbackQuery

bot = Bot(token='1851793811:AAHkSAyxTC8q00qBbGa78c8uNJgvoyrIsws', parse_mode="HTML")
dp = Dispatcher(bot)

but1 = KeyboardButton('Указать почту')
but2 = KeyboardButton('Отмена')
kb_but1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_but1.add(but1)
kb_but1.add(but2)

greeting_callback = CallbackData("answer", "answer_name")

kb1 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да", callback_data=greeting_callback.new(answer_name="Да")),
                InlineKeyboardButton(text="Нет", callback_data=greeting_callback.new(answer_name="Нет")),
            ]
        ]
    )

@dp.message_handler(commands=['start'])
async def process_start_command1(message: types.Message):
    await message.answer(f'{message.chat.username}, привет!\nГотов развиваться?', reply_markup=kb1)

@dp.callback_query_handler(text_contains="Да")
async def answer_yes(call: CallbackQuery):
    '''Заносим пользователя в БД'''
    await call.answer(cache_time=60)
    await call.message.answer("Молодец! Осталось только записаться на сайте http://127.0.0.1:5000/"
                              "\nНе забудь указать почту! (клик по кнопке)", reply_markup=kb_but1)
    user_id = call.from_user.id
    user_name = call.from_user.username
    connect = sqlite3.connect('db_students.db')
    cursor = connect.cursor()
    connect.commit()
    cursor.execute(f'SELECT id FROM Students WHERE id = {user_id}')
    data = cursor.fetchone()
    connect.commit()
    if data is None:
        cursor.execute("INSERT INTO Students VALUES(?,?,?,?);", (user_id,user_name, None, 1))
        connect.commit()
    else: print("Такой пользователь уже существует")

@dp.callback_query_handler(text_contains="Нет")
async def answer_no(call: CallbackQuery):
    '''Заносим пользователя в БД'''
    await call.answer(cache_time=60)
    await call.message.answer("Хм, а может стоит подробнее почитать информацию на сайте: http://127.0.0.1:5000/ ?")
    user_id = call.from_user.id
    user_name = call.from_user.username
    connect = sqlite3.connect('db_students.db')
    cursor = connect.cursor()
    connect.commit()
    cursor.execute(f'SELECT id FROM Students WHERE id = {user_id}')
    data = cursor.fetchone()
    connect.commit()
    if data is None:
        cursor.execute("INSERT INTO Students VALUES(?,?,?,?);", (user_id,user_name, None, 0))
        connect.commit()
    else: print("Такой пользователь уже существует")

'''Стираем все в БД по пользователю'''
@dp.message_handler(commands=['deleteme'])
async def process_help_command(message: types.Message):
    connect = sqlite3.connect('db_students.db')
    cursor = connect.cursor()
    user_id = message.chat.id
    cursor.execute(f'DELETE FROM Students WHERE id = {user_id}')
    connect.commit()
'''Отправка почты с занесением в БД'''
@dp.message_handler(text = 'Указать почту')
async def process_email(msg: types.Message):
    await msg.answer(f'{msg.chat.username}, Введи почту: ')
    @dp.message_handler(content_types=['text'])
    async def handle_text(message: Message):
            user_email = f'{message.text}'
            connect = sqlite3.connect('db_students.db')
            cursor = connect.cursor()
            user_id = f'{message.chat.id}'
            cursor.execute(f'SELECT email FROM Students WHERE id = "{user_id}"')
            email = cursor.fetchone()
            print(email)
            if email[0] != user_email:
                  cursor.execute(f'UPDATE Students SET email = "{user_email}" WHERE id = "{user_id}"')
                  connect.commit()
                  await message.answer(f'{message.chat.username}, Ваша почта внесена в базу!\nЖдите подтверждения на почту!')
            elif email[0] == user_email:
                  await message.answer(f'{message.chat.username}, Эта почта уже используется!\nПопробуйте другую!')

if __name__ == '__main__':
    executor.start_polling(dp)


