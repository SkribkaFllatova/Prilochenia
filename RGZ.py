import asyncio
import logging
import psycopg2
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
import requests
import decimal

logging.basicConfig(level=logging.INFO)
bot = Bot(token="6850439811:AAFml9Z7gIs1MsEoGHuFgqqSsn41ErOwBDY")
dp = Dispatcher()

#Подключение к базе данных
conn = psycopg2.connect(
  host="localhost",
  database="rgz",
  user='rgz',
  password="12345"
)

cursor = conn.cursor()


class RegState(StatesGroup):
    waiting_for_login = State()

class OperationState(StatesGroup):
    waiting_for_type = State()
    waiting_for_amount = State()
    waiting_for_date = State()

class CheckOperationsState(StatesGroup):
    waiting_for_currency = State()
    waiting_for_date_from = State()
    waiting_for_date_by = State()

currency_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="RUB"), KeyboardButton(text="EUR"), KeyboardButton(text="USD")]
    ],
    resize_keyboard=True
)

operation_type_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="РАСХОД"), KeyboardButton(text="ДОХОД")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Команда /reg - для регистрации, /add_operation - для добавления новой операции, /operations - для просмотра операций")

@dp.message(Command("reg"))
async def register_user(message: types.Message, state: FSMContext):
    cursor.execute('SELECT * FROM users WHERE chat_id=%s', (message.chat.id,))
    user = cursor.fetchone()
    if user:
        await message.answer("Вы зарегистрированы")
    else:
        await message.answer("Введите ваш логин:")
        await state.set_state(RegState.waiting_for_login)


@dp.message(RegState.waiting_for_login)
async def process_login(message: types.Message, state: FSMContext):
    login = message.text
    cursor.execute('INSERT INTO users (name, chat_id) VALUES (%s, %s)', (login, message.chat.id,))
    conn.commit()
    await message.answer(f"{login}, Вы успешно зарегистрированы")
    await state.clear()


@dp.message(Command("add_operation"))
async def add_operation(message: types.Message, state: FSMContext):
    cursor.execute('SELECT * FROM users WHERE chat_id=%s', (message.chat.id,))
    user = cursor.fetchone()
    if not user:
        await message.answer("Вы не зарегистрированы, введите команду /reg и зарегиструетесь")
        return

    await message.answer("Выберите тип операции:", reply_markup=operation_type_keyboard)
    await state.set_state(OperationState.waiting_for_type)


@dp.message(OperationState.waiting_for_type)
async def process_operation_type(message: types.Message, state: FSMContext):
    operation_type = message.text.upper()
    if operation_type not in ["РАСХОД", "ДОХОД"]:
        await message.answer("Пожалуйста, выберите тип операции")
        return

    await state.update_data(operation_type=operation_type)
    await message.answer("Введите сумму операции в рублях:")
    await state.set_state(OperationState.waiting_for_amount)


@dp.message(OperationState.waiting_for_amount)
async def process_operation_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите корректную сумму в рублях.")
        return

    await state.update_data(amount=amount)
    await message.answer("Укажите дату операции в формате ГГГГ-ММ-ДД:")
    await state.set_state(OperationState.waiting_for_date)


@dp.message(OperationState.waiting_for_date)
async def process_operation_date(message: types.Message, state: FSMContext):
    try:
        operation_date = datetime.strptime(message.text, "%Y-%m-%d").date()
    except ValueError:
        await message.answer("Введите корректную дату в формате ГГГГ-ММ-ДД")
        return

    user_data = await state.get_data()
    type_operation = user_data['operation_type']
    amount = user_data['amount']

    cursor.execute(
        'INSERT INTO operations (date, sum, chat_id, type_operation) VALUES (%s, %s, %s, %s)',
        (operation_date, amount, message.chat.id, type_operation)
    )
    conn.commit()

    await message.answer(f"Операция добавлена: {type_operation} на сумму {amount} рублей от {operation_date}.")
    await state.clear()


@dp.message(Command("operations"))
async def view_operations(message: types.Message, state: FSMContext):
    cursor.execute('SELECT * FROM users WHERE chat_id=%s', (message.chat.id,))
    user = cursor.fetchone()
    if not user:
        await message.answer("Вы не зарегистрированы, введите команду /reg и зарегиструетесь")
        return

    await message.answer("Введите дату начала периода в формате ГГГГ-ММ-ДД:")
    await state.set_state(CheckOperationsState.waiting_for_date_from)


@dp.message(CheckOperationsState.waiting_for_date_from)
async def date_from_handler(message: types.Message, state: FSMContext):
    try:
        date_from = datetime.strptime(message.text, "%Y-%m-%d").date()
    except ValueError:
        await message.answer("Неверный формат даты. Введите дату в формате ГГГГ-MM-ДД.")
        return 
    await message.answer("Введите дату окончания периода в формате ГГГГ-MM-ДД:")
    await state.set_state(CheckOperationsState.waiting_for_date_by) 

@dp.message(CheckOperationsState.waiting_for_date_by)
async def date_to_handler(message: types.Message, state: FSMContext):
    try:
        date_by = datetime.strptime(message.text, "%Y-%m-%d").date()
    except ValueError:
        await message.answer("Неверный формат даты. Введите дату в формате ГГГГ-MM-ДД.")
        return 

    await message.answer("Выберите валюту для просмотра операций:", reply_markup=currency_keyboard)
    await state.set_state(CheckOperationsState.waiting_for_currency)


@dp.message(CheckOperationsState.waiting_for_currency)
async def process_currency_choice(message: types.Message, state: FSMContext):
    data = await state.get_data()
    date_from = data.get('date_from')
    date_by = data.get('date_by')
    currency = message.text.upper()
    if currency not in ["RUB", "EUR", "USD"]:
        await message.reply("Выберите валюту, нажав на кнопку")
        return

    await state.update_data(currency=currency)

    if currency in ["EUR", "USD"]:
        rate = get_exchange_rate(currency)
        if not rate:
            await message.reply("Не удалось получить актуальный курс валют.")
            await state.clear()
            return
        rate = decimal.Decimal(rate)
    else:
        rate = decimal.Decimal(1)

    cursor.execute('SELECT * FROM operations WHERE date BETWEEN %s AND %s', (date_from, date_by))

    operations = cursor.fetchall()

    if not operations:
        await message.reply("У вас нет операций")
        await state.clear()
        return

    response = "Ваши операции:\n"
    for operation in operations:
        operation_id, operation_date, amount, chat_id, operation_type = operation
        converted_amount = amount / rate
        response += f"{operation_date}: {operation_type} {converted_amount:.2f} {currency}\n"

    await message.reply(response)
    await state.clear()


def get_exchange_rate(currency):
    url = f"http://89.191.225.19:8000/rate?currency={currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['rate']
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 400:
            print(f"Ошибка 400: UNKNOWN CURRENCY: {http_err}")
        elif response.status_code == 500:
            print(f"Ошибка 500: UNEXPECTED ERROR: {http_err}")
        return None
    except Exception as err:
        print(f"Курс валют не удалось получить: {err}")
        return None

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
