from flask import Flask, request, jsonify 
import psycopg2 
app = Flask(__name__) 


conn = psycopg2.connect( 
  dbname="lab6", 
  user="lab6", 
  password="12345", 
  host="localhost", 
)

#Эндпоинт для загрузки новой валюты
@app.route('/load', methods=['POST']) 
def load_currency():
  with conn.cursor() as cursor: 
    try:
      data = request.get_json() #Получаем JSON-данные из запроса
      currency_name = data.get('currency_name') #Извлекаем имя валюты из JSON
      rate = data.get('rate') #Извлекаем курс валюты из JSON
      if not currency_name or not rate: 
        return jsonify({"message": "Invalid JSON data"}), 400 #Возвращаем сообщение об ошибке 400, если не указано имя валюты
      cursor.execute("SELECT * FROM currencies WHERE currency_name = %s", (currency_name,)) 
      existing_currency = cursor.fetchone() 
      if existing_currency: 
        return jsonify({"message": "Currency already exists"}), 400 #Возвращаем сообщение об ошибке 400, если валюта уже есть в бд
      cursor.execute("INSERT INTO currencies (currency_name, rate) VALUES (%s, %s)", (currency_name, rate)) #запрос на добавление новой валюты
      conn.commit()
      return jsonify({"message": "Currency loaded successfully"}), 200 #Возвращаем сообщение об успешной загрузке валюты
    except psycopg2.Error as e: 
      conn.rollback() 
      return jsonify({"message": f"Database error: {str(e)}"}), 500 #Возвращаем сообщение об ошибке 500, если произошла ошибка

#Эндпоинт для обновления курса валюты
@app.route('/update_currency', methods=['POST']) 
def update_currency():
  with conn.cursor() as cursor:
    try:
      data = request.get_json() #Получаем JSON-данные из запроса
      currency_name = data.get('currency_name') #Извлекаем имя валюты из JSON
      new_rate = data.get('rate') #Извлекаем новый курс валюты из JSON
      if not currency_name or not new_rate: 
        return jsonify({"message": "Invalid JSON data"}), 400 
      #Проверка существования валюты в БД
      cursor.execute("SELECT * FROM currencies WHERE currency_name = %s", (currency_name,)) 
      existing_currency = cursor.fetchone() #Получаем результат запроса
      if not existing_currency: 
        return jsonify({"message": "Currency not found"}), 404 
      cursor.execute("UPDATE currencies SET rate = %s WHERE currency_name = %s", (new_rate, currency_name)) #Выполняем запрос на обновление курса валюты
      conn.commit() 
      return jsonify({"message": "Currency updated successfully"}), 200 #Возвращаем сообщение об успешном обновлении валюты
    except psycopg2.Error as e: 
      conn.rollback() 
      return jsonify({"message": f"Database error: {str(e)}"}), 500 
      
#Эндпоинт для удаления валюты
@app.route('/delete', methods=['POST']) #Объявляем эндпоинт для обработки POST-запросов на адрес '/delete'
def delete_currency():
  with conn.cursor() as cursor: 
    try:
      data = request.get_json() 
      currency_name = data.get('currency_name') 
      if not currency_name: 
        return jsonify({"message": "Invalid JSON data"}), 400 
      cursor.execute("SELECT * FROM currencies WHERE currency_name = %s", (currency_name,)) #Выполняем запрос к базе данных для проверки существования валюты
      existing_currency = cursor.fetchone()
      if not existing_currency:
        return jsonify({"message": "Currency not found"}), 404
      cursor.execute("DELETE FROM currencies WHERE currency_name = %s", (currency_name,)) #Выполняем запрос на удаление валюты
      conn.commit() 
      return jsonify({"message": "Currency deleted successfully"}), 200 
    except psycopg2.Error as e:
      conn.rollback() 
      return jsonify({"message": f"Database error: {str(e)}"}), 500 


if __name__ == '__main__': 
  app.run(port=5001) #Запускаем Flask-приложение на порту 5001