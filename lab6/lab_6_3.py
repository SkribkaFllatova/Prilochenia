from flask import Flask, request, jsonify 
import psycopg2 
app = Flask(__name__) 


def get_cursor():
  conn = psycopg2.connect( 
    dbname="lab6", 
    user="lab6", 
    password="12345", 
    host="localhost", 
  )

  cursor = conn.cursor() 
  return conn, cursor 

#Эндпоинт для конвертации валюты
@app.route('/convert', methods=['GET']) #Объявляем эндпоинт для обработки GET-запросов на адрес '/convert'
def convert_currency():
  currency_name = request.args.get('currency_name') 
  amount = float(request.args.get('amount')) # Получаем сумму для конвертации из параметра запроса и преобразуем её в тип float.
  try:
    conn, cursor = get_cursor()
    cursor.execute("SELECT rate FROM currencies WHERE currency_name = %s", (currency_name,)) #Выполняем запрос к базе данных для получения курса валюты
    existing_currency = cursor.fetchone() 
    if not existing_currency:
      return jsonify({"message": "Currency not found"}), 404 
    rate = existing_currency[0] #Извлекаем курс валюты из результата запроса
    #Конвертация суммы
    converted_amount = amount * float(rate) #Вычисляем сконвертированную сумму
    return jsonify({"converted_amount": converted_amount}), 200 #Возвращаем сконвертированную сумму в формате JSON с кодом состояния 200
  except psycopg2.Error as e: 
    return jsonify({"message": f"Database error: {str(e)}"}), 500 
  finally:
    cursor.close() #Закрываем курсор
    conn.close() #Закрываем соединение

#Эндпоинт для получения списка всех валют
@app.route('/currencies', methods=['GET']) #Объявляем эндпоинт для обработки GET-запросов на адрес '/currencies'
def get_currencies():
  try:
    conn, cursor = get_cursor() #Получаем соединение и курсор
    cursor.execute("SELECT currency_name FROM currencies") #Выполняем запрос к базе данных для получения списка всех валют
    currencies = [row[0] for row in cursor.fetchall()] #Извлекаем имена валют из результатов запроса
    return jsonify({"currencies": currencies}), 200 #Возвращаем список всех валют в формате JSON с кодом состояния 200
  except psycopg2.Error as e:
    return jsonify({"message": f"Database error: {str(e)}"}), 500 
  finally:
    cursor.close() #Закрываем курсор
    conn.close() #Закрываем соединение


if __name__ == '__main__':
  app.run(port=5002) # Запускаем Flask-приложение на порту 5002.