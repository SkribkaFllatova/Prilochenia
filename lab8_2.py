import asyncio #Библиотека для асинхронного программирования
import json # Библиотека для работы с JSON-данными
from collections import defaultdict
#Импортируем класс defaultdict из модуля collections
#defaultdict – это словарь, который автоматически создает новые ключи со значением по умолчанию (в данном случае – 0.0), если ключ отсутствует.

limit = 10000.0 #Задает переменную limit, представляющую собой лимит расходов (5000.0 рублей)

async def read_transactions_from_file(filename): #Определяем асинхронную функцию read_transactions_from_file, 
#которая принимает имя файла в качестве аргумента. Эта функция предназначена для чтения транзакций из файла.
    with open(filename, 'r', encoding='utf-8') as file: #Открываем указанный файл в режиме чтения ('r') с кодировкой UTF-8.  
        for line in file: #Перебираем каждую строку в файле
            transaction = json.loads(line.strip())
#Преобразуем каждую строку (после удаления начальных и конечных пробелов с помощью .strip()) из JSON-формата в словарь Python
            yield transaction
#Возвращаем обработанную транзакцию с помощью генератора. Это позволяет обрабатывать данные по одной транзакции за раз, не загружая весь файл в память сразу

async def process_transactions(filename): #Определяем асинхронную функцию process_transactions, которая обрабатывает транзакции из файла
    category_totals = defaultdict(float)  
#Создаем словарь category_totals с использованием defaultdict, где ключи – категории расходов, а значения – суммы расходов по каждой категории (изначально 0.0)
    limit_reached = set() #Создаем множество limit_reached, которое будет хранить категории, по которым лимит расходов уже превышен.  

    async for transaction in read_transactions_from_file(filename): #Асинхронный цикл, который перебирает транзакции, полученные из функции`read_transactions_from_file
        category = transaction['category'] #Извлекаем категорию расходов из текущей транзакции
        amount = transaction['amount'] #Извлекаем сумму расходов из текущей транзакции
        category_totals[category] += amount #Добавляем сумму amount к текущей сумме расходов в категории category
        
        if category_totals[category] > limit and category not in limit_reached: #Проверяем, превышает ли сумма расходов по категории лимит, и была ли эта категория уже отмечена как превысившая лимит.

            print(f"Расходы в {category} превысили установленный лимит {limit}: {category_totals[category]}") #Выводит сообщение о превышении лимита
            limit_reached.add(category) #Добавляем категорию в множество limit_reached

    for category, total in category_totals.items(): #Цикл, перебирающий категории и их общие суммы расходов
        print(f"Расходы в категории {category} составили: {total:.2f} руб.") #Выводим общие расходы по каждой категории, форматируя сумму до двух десятичных знаков

async def main(filename): #Определяем асинхронную функцию main, которая запускает обработку транзакций
    await process_transactions(filename) #Запускаем асинхронную функцию process_transactions

if __name__ == "__main__": 
    filename = "transactions.json" #Задаем имя файла с транзакциями
    asyncio.run(main(filename)) #Запускаем асинхронную функцию main
