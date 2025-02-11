from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import asyncio
import random
import string

api_token = ''
bot = Bot(token=api_token)
dp = Dispatcher()

password_db = {}

def gen_password(length=12):
    charct = string.ascii_letters + string.digits + string.punctuation
    passw = ''.join(random.choice(charct) for i in range(length))
    return passw

def save_password(user_id, password, purpose):
    if user_id not in password_db:
        password_db[user_id] = []
    password_db[user_id].insert(0, (password, purpose))

main_button1 = KeyboardButton(text = "Генерация")
main_button2 = KeyboardButton(text = "Библиотека")
main_button3 = KeyboardButton(text = "Отмена")
main_keyboard = ReplyKeyboardMarkup(keyboard=[[main_button1], [main_button2], [main_button3]], resize_keyboard=True)

@dp.message(Command('start'))
async def start_command(message: Message):
    await message.answer('Привет! Я бот который генерирует случайные и безопасные пароли\nВыберите дейсвие для начала работы: ', reply_markup=main_keyboard)


@dp.message(F.text == "Генерация")
async def generate_command(message:Message):
    await message.answer("Укажите длину пароля (8-32):")

@dp.message(F.text, lambda message: message.text.isdigit() and 8 <= int(message.text) <= 32)
async def process_length(message: Message):
     length = int(message.text)
     dp.current_length = length
     await message.answer("Для чего нужен пароль?", reply_markup=main_keyboard)

@dp.message(F.text)
async def process_purpose(message:Message):
     purpose = message.text
     password = gen_password()
     user_id = message.from_user.id
     save_password(user_id, password, purpose)
     await message.answer("Ваш пароль сохранено!", reply_markup=main_keyboard)


@dp.message(F.text == "Библиотека")
async def library_command(message: Message):
    user_id = message.from_user.id
    passwords = password_db.get(user_id, [])

    if passwords:
        response = "Ваши сохраненные пароли:\n"
        for password, purpose in passwords:
            response += f"Пароль: `{password}`\nДля: {purpose or 'Не указано'}\n"
        await message.answer(response, parse_mode="Markdown")
    else:
        await message.answer("Ваша библиотека паролей пуста.", reply_markup=main_keyboard)


@dp.message(F.text == "Отмена")
async def cancel_command(message: Message):
    await message.answer("Действие отменено.", reply_markup=main_keyboard)

async def main():
    print('Бот запущен')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())