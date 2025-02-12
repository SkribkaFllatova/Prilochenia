import asyncio #Библиотека для асинхронного программирования
import json #Библиотека для работы с JSON-данными
import random #Библиотека для генерации случайных чисел
from datetime import datetime, timedelta #Библиотеки для работы с датами и временем

async def generate_transaction(): 
    start_date = datetime(2024, 1, 1)  
    end_date = datetime(2024, 12, 31)  #Устанавливаем начальную и конечную даты (с 1 января по 31 декабря 2024 года)
    random_date = start_date + timedelta( #Генерируем случайную дату в этом промежутке
        seconds=random.randint(0, int((end_date - start_date).total_seconds()))
    )
    return { #Возвращаем словарь, представляющий транзакцию
        "timestamp": random_date.isoformat(), #метка времени (ISO формат), 
        "category": random.choice(["Транспорт", "Супермаркеты", "Кафе и рестораны"]), #категория (случайная из списка), 
        "amount": round(random.uniform(100.0, 5000.0), 2), #сумма (случайное число от 100 до 5000 с двумя знаками после запятой)
    }

async def save_to_file(transactions, filename="transactions.json"): #Принимаем список транзакций и имя файла (по умолчанию "transactions.json")
    with open(filename, "a", encoding="utf-8") as file: #Открываем файл в режиме добавления ("a")
        for transaction in transactions:
            file.write(json.dumps(transaction, ensure_ascii=False) + "\n") #Записываем каждую транзакцию в файл в формате JSON
    print(f"Сохранено {len(transactions)} транзакций в файл: {filename}") #Выводим сообщение о количестве сохраненных транзакций.

async def generate_transactions(total_count, filename="transactions.json"): #Принимаем общее количество транзакций и имя файла.
    tasks = [] #Создаем пустые списки tasks (для задач) и transactions (для транзакций)
    transactions = []

    for i in range(total_count):
        tasks.append(asyncio.create_task(generate_transaction())) # Создаем задачу генерации транзакции с помощью asyncio.create_task()
        if (i + 1) % 10 == 0 or i == total_count - 1:  #Добавляем задачу в список tasks
            transactions.extend(await asyncio.gather(*tasks)) #После каждых 10 транзакций (или после последней) ожидает завершения всех задач в tasks с помощью asyncio.gather()
#Добавляем полученные транзакции в transactions
            await save_to_file(transactions, filename) #Сохраняем транзакции в файл с помощью save_to_file()
            transactions.clear()   #Очищаем списки tasks и transactions
            tasks.clear()

if __name__ == "__main__":
    count = int(input("Укажите количество транкзаций ")) #Запрашиваем количество транзакций
    asyncio.run(generate_transactions(count)) #Запускаем асинхронную функцию generate_transactions() с помощью asyncio.run()