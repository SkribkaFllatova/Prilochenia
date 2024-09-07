import logging # Импорт модуля logging для ведения журналирования (логирования) событий
from aiogram import Bot, Dispatcher, executor, types 
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import requests
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv # Импорт функции load_dotenv для загрузки переменных окружения из файла .env
import os
from token import TOKEN_API 
# Загрузка переменных окружения из файла .env
load_dotenv()
logging.basicConfig(level=logging.INFO) # Настройка базового конфигурационного параметра для логирования (уровень INFO)

bot_token = os.getenv(TOKEN_API) 
dp = Dispatcher(bot, storage=MemoryStorage())

# URL-адреса для микросервисов currency-manager и data-manager
CURRENCY_MANAGER_URL = 'http://localhost:5001'
DATA_MANAGER_URL = 'http://localhost:5002'


class AddCurrency(StatesGroup): #Группа состояний для добавления валюты
  currency_name = State() #Ввод имени валюты
  currency_rate = State() #Ввод курса валюты


class DeleteCurrency(StatesGroup): #... для удаления валюты
  currency_name = State() #Ввод имени валюты


class UpdateCurrency(StatesGroup): #... для изменения курса валюты
  currency_name = State() #Ввод имени валюты
  new_rate = State() #Ввод нового курса валюты


class ConvertCurrency(StatesGroup): #... для конвертации суммы
  currency_name = State() #Выбор валюты конвертации
  amount = State() #Ввод суммы конвертации


#Обработчик команды /start
@dp.message_handler(commands=['start']) 
async def start(message: types.Message): 
  await message.answer("Привет! Набери /manage_currency, чтобы начать работу с валютами.") 


#Обработчик команды /manage_currency
@dp.message_handler(commands=['manage_currency']) 
async def manage_currency(message: types.Message): 
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True) #Создание объекта ReplyKeyboardMarkup для создания клавиатуры
  keyboard.add(types.KeyboardButton("Добавить валюту")) #Добавление кнопки "Добавить валюту" на клавиатуру
  keyboard.add(types.KeyboardButton("Удалить валюту")) #Добавление кнопки "Удалить валюту" на клавиатуру
  keyboard.add(types.KeyboardButton("Изменить курс валюты")) #Добавление кнопки "Изменить курс валюты" на клавиатуру
  await message.answer("Выбери команду:", reply_markup=keyboard) 

#Обработчик кнопки "Добавить валюту"
@dp.message_handler(lambda message: message.text == "Добавить валюту") 
async def add_currency(message: types.Message):
  await message.answer("Введите название валюты:") 
  await AddCurrency.currency_name.set() # Установка состояния FSM для ввода названия валюты

#Обработчик ввода названия валюты
@dp.message_handler(state=AddCurrency.currency_name) 
async def process_currency_name(message: types.Message, state: FSMContext):
  async with state.proxy() as data: #Получение данных из состояния FSM
    data['currency_name'] = message.text #Сохранение введенного пользователем названия валюты
  #Проверка существования введенной валюты
  response = requests.get(f"{DATA_MANAGER_URL}/currencies") #Отправка запроса на получение списка валют
  try:
    currencies = response.json()['currencies'] 
  except Exception as e:
    print("Error:", e) 
    await message.answer("Ошибка получения данных о валютах")
    await state.finish() 
    return
  if data['currency_name'] in currencies: 
    await message.answer("Данная валюта уже существует") 
    await state.finish()
    return
  await message.answer("Введите курс к рублю:") 
  await AddCurrency.currency_rate.set() 

#Обработчик ввода курса валюты
@dp.message_handler(state=AddCurrency.currency_rate) 
async def process_currency_rate(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['rate'] = float(message.text) 
  #Отправка запроса на сохранение валюты
  response = requests.post(f"{CURRENCY_MANAGER_URL}/load", json={"currency_name": data['currency_name'], "rate": data['rate']})
  if response.status_code == 200: #Проверка успешности запроса
    await message.answer(f"Валюта {data['currency_name']} успешно добавлена")
  else:
    await message.answer("Ошибка добавления валюты") 
  await state.finish()


#Обработчик кнопки "Удалить валюту"
@dp.message_handler(lambda message: message.text == "Удалить валюту") 
async def delete_currency(message: types.Message):
  await message.answer("Введите название валюты для удаления:") 
  await DeleteCurrency.currency_name.set() 

#Обработчик ввода названия валюты для удаления
@dp.message_handler(state=DeleteCurrency.currency_name)
async def process_delete_currency_name(message: types.Message, state: FSMContext):
  async with state.proxy() as data: 
    data['currency_name'] = message.text 
  response = requests.post(f"{CURRENCY_MANAGER_URL}/delete", json={"currency_name": data['currency_name']}) #Отправка запроса на удаление валюты
  if response.status_code == 200:
    await message.answer(f"Валюта {data['currency_name']} успешно удалена") #Отправка сообщения об успешном удалении валюты
  else:
    await message.answer("Ошибка удаления валюты") 
  await state.finish()

#Обработчик кнопки "Изменить курс валюты"
@dp.message_handler(lambda message: message.text == "Изменить курс валюты") 
async def update_currency(message: types.Message):
  await message.answer("Введите название валюты для изменения курса:") 
  await UpdateCurrency.currency_name.set() 

#Обработчик ввода названия валюты для изменения курса
@dp.message_handler(state=UpdateCurrency.currency_name) 
async def process_update_currency_name(message: types.Message, state: FSMContext): 
  async with state.proxy() as data:
    data['currency_name'] = message.text 
  await message.answer("Введите новый курс к рублю:") 
  await UpdateCurrency.new_rate.set() 

#Обработчик ввода нового курса валюты
@dp.message_handler(state=UpdateCurrency.new_rate)
async def process_update_currency_rate(message: types.Message, state: FSMContext):
  async with state.proxy() as data: 
    data['new_rate'] = float(message.text) 
  response = requests.post(f"{CURRENCY_MANAGER_URL}/update_currency", json={"currency_name": data['currency_name'], "rate": data['new_rate']}) 
  #Отправка запроса на обновление курса валюты
  if response.status_code == 200:
    await message.answer(f"Курс валюты {data['currency_name']} успешно изменен") 
  else:
    await message.answer("Ошибка изменения курса валюты")
  await state.finish() 

#Обработчик команды /get_currencies
@dp.message_handler(commands=['get_currencies']) 
async def get_currencies(message: types.Message): 
  response = requests.get(f"{DATA_MANAGER_URL}/currencies") #Отправка запроса на получение списка валют
  try:
    currencies = response.json()['currencies'] #Получение списка валют из ответа
  except Exception as e: 
    print("Error:", e) 
    await message.answer("Ошибка получения данных о валютах") 
    return
  if currencies: 
    currencies_list = "\n".join(currencies) #Формирование строки с перечислением валют
    await message.answer(f"Список доступных валют:\n{currencies_list}") 
  else:
    await message.answer("Нет сохраненных валют") 

#Обработчик команды /convert
@dp.message_handler(commands=['convert']) 
async def convert_currency(message: types.Message): 
  await message.answer("Введите название валюты для конвертации:") 
  await ConvertCurrency.currency_name.set() 

#Обработчик ввода названия валюты для конвертации
@dp.message_handler(state=ConvertCurrency.currency_name) 
async def process_convert_currency_name(message: types.Message, state: FSMContext):
  async with state.proxy() as data: 
    data['currency_name'] = message.text 
  await message.answer("Введите сумму:") 
  await ConvertCurrency.amount.set()

#Обработчик ввода суммы для конвертации
@dp.message_handler(state=ConvertCurrency.amount) 
async def process_convert_amount(message: types.Message, state: FSMContext): 
  async with state.proxy() as data: 
    data['amount'] = float(message.text) 
  #Отправляем запрос на конвертацию суммы
  response = requests.get(f"{DATA_MANAGER_URL}/convert", params={"currency_name": data['currency_name'], "amount": data['amount']})
  if response.status_code == 200: 
    try:
      converted_amount = response.json().get('converted_amount') #Получение сконвертированной суммы из ответа
      if converted_amount is not None: 
        await message.answer(f"Конвертированная сумма: {converted_amount} руб.") 
      else:
        await message.answer("Ошибка при конвертации") 
    except Exception as e:
      print("Error:", e)
      await message.answer(f"Ошибка при конвертации: {e}") 
  else:
    await message.answer(f"Произошла ошибка при конвертации суммы: статус {response.status_code}") 
# Отправка сообщения об ошибке при статусе запроса, отличном от 200
  await state.finish()
 
#Меню команд
@dp.message_handler(commands=['start', 'manage_currency', 'get_currencies', 'convert']) 
async def process_commands(message: types.Message): 
  if message.text == '/start': #Проверка команды /start
    await start(message) #Вызов функции-обработчика команды /start
  elif message.text == '/manage_currency': 
    await manage_currency(message) 
  elif message.text == '/get_currencies': 
    await get_currencies(message) 
  elif message.text == '/convert': 
    await convert_currency(message) 

#Обработчик команды /menu
@dp.message_handler(commands=['menu']) 
async def show_menu(message: types.Message): 
  keyboard = ReplyKeyboardMarkup(resize_keyboard=True) #Создание клавиатуры для меню
  keyboard.add(KeyboardButton("/manage_currency")) #Добавление кнопки "Управление валютами(добавление, удаление,конвертация)"
  keyboard.add(KeyboardButton("/get_currencies")) #Добавление кнопки "Получение списка валют"
  keyboard.add(KeyboardButton("/convert")) #Добавление кнопки "Конвертация валюты"
  await message.answer("Выберите действие:", reply_markup=keyboard) 


if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)

