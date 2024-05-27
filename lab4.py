from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from token import TOKEN_API
import logging
import os

logging.basicConfig(level=logging.INFO) 

bot_token = os.getenv(TOKEN_API)


dp = Dispatcher(bot, storage=MemoryStorage())

class Form(StatesGroup):
    name = State()  
    currency_name = State()  
    currency_rate = State()  
    convert_currency_name = State() 
    convert_amount = State()

currency_data = {}

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await Form.name.set()
    await message.reply("Здравствуй! Напиши команду /save_currency, которая сохраняет курс валюты к рублю . Напиши команду /convert, которая конвертирует указанную сумму заданной валюты в рубли.")


# Задание 1. Создать обработчик для команды /save_currency. 

        # после ввода команды /save_currency бот предлагает ввести название валюты
@dp.message_handler(commands=['save_currency'], state=Form.name)
async def process_save_currency_command(message: types.Message):
    await Form.currency_name.set()
    await message.reply("Введите название валюты:")

        # после ввода названия валюты бот предлагает ввести курс валюты к рублю
@dp.message_handler(state=Form.currency_name)
async def process_currency_name(message: types.Message, state: FSMContext):
    currency_name = message.text
    await Form.currency_rate.set()
    await state.update_data(currency_name=currency_name)
    await message.reply("Введите курс валюты к рублю:")

        # программа сохраняет название валюты и курс в словарь
@dp.message_handler(state=Form.currency_rate)
async def process_currency_rate(message: types.Message, state: FSMContext):
    currency_rate = message.text
    user_data = await state.get_data()
    currency_name = user_data['currency_name']
    currency_data[currency_name] = currency_rate
    await state.finish()
    await message.reply(f"Курс валюты {currency_name} успешно сохранен.")

# Задание 2. Создать обработчик для команды /convert. 

        # после ввода команды /convert бот предлагает ввести название валюты
@dp.message_handler(commands=['convert'], state="*")
async def process_convert_command(message: types.Message):
    await Form.convert_currency_name.set() 
    await message.reply("Введите название валюты, которую вы хотите конвертировать в рубли:")


        # после ввода названия валюты бот предлагает ввести сумму в указанной валюте
@dp.message_handler(state=Form.convert_currency_name)
async def process_convert_currency_name(message: types.Message, state: FSMContext):
    convert_currency_name = message.text
    await Form.convert_amount.set()
    await state.update_data(convert_currency_name=convert_currency_name)
    await message.reply("Введите сумму в указанной валюте:")

        # бот конвертирует указанную пользователем сумму в рубли по ранее сохраненному курсу выбранной валюты
@dp.message_handler(state=Form.convert_amount)
async def process_convert_amount(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    convert_currency_name = user_data['convert_currency_name']
    convert_amount = float(message.text)
    if convert_currency_name in currency_data:
        currency_rate = float(currency_data[convert_currency_name])
        converted_amount = convert_amount * currency_rate
        await state.finish()
        await message.reply(f"{convert_amount} {convert_currency_name} равно {converted_amount} рублей.")
    else:
        await state.finish()
        await message.reply(f"Курс для валюты {convert_currency_name} не найден.")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dp.middleware.setup(LoggingMiddleware())
    executor.start_polling(dp, skip_updates=True)