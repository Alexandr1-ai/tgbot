from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import asyncio
import random
import string

api_token = '7901672957:AAH9IvywfHx_OFSVnLBaRKwrZXktuvtOF2o'
bot = Bot(token=api_token)
dp = Dispatcher()

password_db = {}
users_state = {}

def gen_password(length):
    charct = string.ascii_letters + string.digits + string.punctuation
    passw = ''.join(random.choice(charct) for i in range(length))
    return passw

def save_password(user_id, password, purpose, length):
    if user_id not in password_db:
        password_db[user_id] = []
    password_db[user_id].insert(0, (password, purpose, length))

main_button1 = KeyboardButton(text = "Генерация")
main_button2 = KeyboardButton(text = "Библиотека")
main_button3 = KeyboardButton(text = "Отмена")
main_keyboard = ReplyKeyboardMarkup(keyboard=[[main_button1], [main_button2]], resize_keyboard=True)
cancel = ReplyKeyboardMarkup(keyboard=[[main_button3]], resize_keyboard=True)

@dp.message(Command('start'))
async def start_command(message: Message):
    await message.answer('Привет! Я бот который генерирует случайные и безопасные пароли'
                         '\nДля продолжения работы выберите действие: ', reply_markup=main_keyboard)


@dp.message(F.text == "Генерация")
async def generate_command(message: Message):
    await message.answer("Укажите длину пароля (8-32):", reply_markup=cancel)

@dp.message(F.text, lambda message: message.text.isdigit() and 8 <= int(message.text) <= 32)
async def process_length(message: Message):
    user_id = message.from_user.id
    length = int(message.text)
    users_state[user_id] = length
    await message.answer('Для чего будет использоваться пароль?', reply_markup=cancel)

    @dp.message(F.text)
    async def process_purpose(message: Message):
        user_id = message.from_user.id
        purpose = message.text
        length = users_state[user_id]
        password = gen_password(length)
        save_password(user_id, password, purpose, length)
        await message.answer(f'Ваш пароль: `{password}`\nСохранен', parse_mode="Markdown", reply_markup=main_keyboard)
        del users_state[user_id]

@dp.message(F.text == "Библиотека")
async def library_command(message: Message):
    user_id = message.from_user.id
    passwords = password_db.get(user_id, [])
    if passwords:
        response = "Ваши сохраненные пароли:\n"
        for password, purpose, length in passwords:
            response += f"- Пароль: '{password}'\nДля: {purpose or 'Не указано'}\n"
        await message.answer(response, reply_markup=main_keyboard)
    else:
        await message.answer("Ваша библиотека паролей пуста", reply_markup=main_keyboard)

@dp.message(F.text == 'Отмена')
async def cancel_command(message:Message):
    await message.answer('Действие отменено')

async def main():
    print('Бот запущен')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())