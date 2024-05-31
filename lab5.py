import asyncio 
import aiogram 
import psycopg2 
from aiogram import Bot, Dispatcher, types 
from aiogram.contrib.fsm_storage.memory import MemoryStorage 
from aiogram.dispatcher import FSMContext 
from aiogram.dispatcher.filters.state import State, StatesGroup 
from aiogram.utils import executor 
import os
import token

conn = psycopg2.connect(
  host="localhost",
  database="lab5",
  user='lab5',
  password='12345'
)

cur = conn.cursor() 


bot_token = os.getenv(TOKEN_API) 

dp = Dispatcher(bot, storage=MemoryStorage()) 


class AddCurrencyStep(StatesGroup): #Группа состояний для добавления валюты
  name = State() #Название валюты
  rate = State() #Курса валюты

class DeleteCurrencyStep(StatesGroup): #... удаления валюты
  name = State() 

class ChangeRateStep(StatesGroup): #... изменения курса валюты
  name = State() 
  rate = State() 

class ConvertCurrencyStep(StatesGroup): #... конвертации валюты
  name = State() 
  amount = State() 


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Выберите команду!") 

#Задание 1.

@dp.message_handler(commands=['manage_currency'])
async def manage_currency(message: types.Message):
  admin_chat_id = str(message.chat.id) 
  cursor = conn.cursor() 
  cursor.execute("SELECT * FROM admins WHERE chat_id = %s", (admin_chat_id,)) 
  admin = cursor.fetchone() 
  if admin is None: 
    await message.answer("Нет доступа к команде") #Eсли пользователь не является администратором, то в чат выводится: "Нет доступа к команде"
    return

  #Если пользователь является администратором, то бот отображает 3 кнопки в один ряд: "Добавить валюту", "Удалить валюту", "Изменить курс валюты"

  markup = types.ReplyKeyboardMarkup(row_width=3) 
  button1 = types.KeyboardButton("Добавить валюту")
  button2 = types.KeyboardButton("Удалить валюту") 
  button3 = types.KeyboardButton("Изменить курс валюты") 
  markup.add(button1, button2, button3) 

  await message.answer("Выберите нужную команду", reply_markup=markup) # Отправка сообщения с клавиатурой для выбора действия


@dp.message_handler(lambda message: message.text == "Добавить валюту")
async def add_currency(message: types.Message):
  await message.answer("Введите название валюты") 
  await AddCurrencyStep.name.set() 

@dp.message_handler(state=AddCurrencyStep.name)
async def add_currency_name(message: types.Message, state: FSMContext):
  currency_name = message.text.strip().upper() 
  cursor = conn.cursor() 
  cursor.execute("SELECT * FROM currencies WHERE currency_name = %s", (currency_name,)) 
  if cursor.fetchone() is not None: 
    await message.answer("Данная валюта уже существует") 
    return

  await state.update_data(currency_name=currency_name) 
  await message.answer("Введите курс к рублю") 
  await AddCurrencyStep.next() 

@dp.message_handler(state=AddCurrencyStep.rate)
async def add_rate_step(message: types.Message, state: FSMContext):
  try:
    rate = float(message.text.strip()) 
    data = await state.get_data() 
    currency_name = data.get('currency_name') 
    cursor = conn.cursor() 
    cursor.execute("INSERT INTO currencies (currency_name, rate) VALUES (%s, %s)", (currency_name, rate)) 
    conn.commit() 
    await message.answer(f"Валюта {currency_name} добавлена") 
  except ValueError:
    await message.answer("Валюта не может быть добавлена") 


@dp.message_handler(lambda message: message.text == "Удалить валюту")
async def delete_currency(message: types.Message):
  await message.answer("Введите название валюты") 
  await DeleteCurrencyStep.name.set() 

@dp.message_handler(state=DeleteCurrencyStep.name)
async def delete_currency_name(message: types.Message, state: FSMContext):
  currency_name = message.text.strip().upper() 
  cursor = conn.cursor() 
  cursor.execute("DELETE FROM currencies WHERE currency_name = %s", (currency_name,)) 
  conn.commit() 
  await message.answer(f"Валюта {currency_name} удалена") 
  await state.finish() 

@dp.message_handler(lambda message: message.text == "Изменить курс валюты")
async def change_rate(message: types.Message):
  await message.answer("Введите название валюты")
  await ChangeRateStep.name.set() 

@dp.message_handler(state=ChangeRateStep.name)
async def change_rate_name(message: types.Message, state: FSMContext):
  currency_name = message.text.strip().upper() 
  await state.update_data(currency_name=currency_name) 
  await message.answer("Введите курс к рублю:") 
  await ChangeRateStep.rate.set() 

@dp.message_handler(state=ChangeRateStep.rate)
async def change_rate_value(message: types.Message, state: FSMContext):
  try:
    rate = float(message.text.strip()) 
    data = await state.get_data() 
    currency_name = data.get('currency_name') 
    cursor = conn.cursor() 
    cursor.execute("UPDATE currencies SET rate = %s WHERE currency_name = %s", (rate, currency_name)) 
    conn.commit() 
    await message.answer(f"Курс валюты {currency_name} изменен") 
  except ValueError:
    await message.answer("Курс валюты не удалось изменить") 
  await state.finish() 


#Задание 2. Вывод всех сохраненных валют с курсом к рублю

@dp.message_handler(commands=['get_currencies'])
async def get_currencies(message: types.Message):
  cursor = conn.cursor() 
  cursor.execute("SELECT currency_name, rate FROM currencies") 
  currencies = cursor.fetchall() 
  if currencies: 
    response = "Сохраненные валюты с курсом к рублю:\n" 
    for currency in currencies: 
      response += f"{currency[0]}: {currency[1]}\n" 
  else:
    response = "Не удалось найти сохраненные валюты" 
  await message.answer(response) 

#Задание 3.

@dp.message_handler(commands=['convert'])
async def convert_currency(message: types.Message):
  await message.answer("Введите название валюты:") 
  await ConvertCurrencyStep.name.set() 

@dp.message_handler(state=ConvertCurrencyStep.name)
async def convert_currency_name(message: types.Message, state: FSMContext):
  currency_name = message.text.strip().upper() 
  cursor = conn.cursor() 
  cursor.execute("SELECT rate FROM currencies WHERE currency_name = %s", (currency_name,))
  currency = cursor.fetchone() 
  if currency:
    await state.update_data(rate=currency[0]) 
    await message.answer("Введите сумму") 
    await ConvertCurrencyStep.next() 


@dp.message_handler(state=ConvertCurrencyStep.amount)
async def convert_amount_step(message: types.Message, state: FSMContext):
  try:
    amount = float(message.text.strip()) 
    data = await state.get_data() 
    currency_name = data.get('currency_name') 
    rate = data.get('rate')

    if rate is None: 
      await message.answer("Данная валюта не найдена") 
      await state.finish() 
      return
   
    converted_amount = amount * float(rate) 
    await message.answer(f"{amount} {currency_name} = {converted_amount} рублей") 
  except ValueError:
    await message.answer("Введен некорректный формат суммы") 
  await state.finish() 

#Добавление нового администратора
@dp.message_handler(commands=['add_admin'])
async def add_admin(message: types.Message):
  admin_chat_id = message.chat.id 
  cursor = conn.cursor() 
  cursor.execute("INSERT INTO admins (chat_id) VALUES (%s)", (admin_chat_id,)) 
  conn.commit() 
  await message.answer("Поздравляем! Вы теперь администратор") 


if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True) 
