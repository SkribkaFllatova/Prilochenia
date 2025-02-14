from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import os

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day"] 
    #Создаем экземпляр Limiter, который будет использоваться для ограничения количества запросов
    #В данном случае мы устанавливаем лимит в 100 запросов в день для каждого IP-адреса
)

DATA_FILE = "data.json"
data = {}
#Определяем имя файла, в котором будут храниться данные, и инициализируем пустой словарь data, 
#который будет использоваться для хранения пар "ключ-значение"

def load_data():
    global data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    else:
        data = {}
#Определяем функцию load_data, которая загружает данные из файла data.json
#Если файл существует, он открывается, и данные загружаются в словарь data. Если файл не существует, data остается пустым

def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)
#Определяем функцию save_data, которая сохраняет текущие данные из словаря data в файл data.json. Данные записываются в формате JSON

load_data()
#Вызываем функцию load_data, чтобы загрузить данные из файла при запуске приложения

@limiter.limit("10 per minute", methods=["POST"])
@app.route("/set", methods=["POST"])
def set_key(): #Определяем маршрут /set, который принимает POST-запросы. Устанавливаем лимит на 10 запросов в минуту для этого маршрута
    request_data = request.get_json() #Получаем данные из тела запроса в формате JSON
    key = request_data.get("key") #Извлекаем значения key и value из полученных данных
    value = request_data.get("value")

    if not key or value is None:
        return jsonify({"error": "Both 'key' and 'value' must be provided."}), 400
#Проверяем, что оба значения (ключ и значение) предоставлены. Если одно из них отсутствует, возвращаем ошибку с кодом 400 (Bad Request)
    data[key] = value #Сохраняем пару "ключ-значение" в словаре data
    save_data() #Вызываем функцию save_data, чтобы сохранить обновленные данные в файл
    return jsonify({"message": "Key-Value pair saved successfully."}), 200 #Возвращаем успешный ответ с сообщением и кодом 200 (OK)

@app.route("/get/<key>", methods=["GET"])
def get_key(key): #Определяем маршрут /get/<key>, который принимает GET-запросы и позволяет получить значение по указанному ключу
    value = data.get(key) #Извлекаем значение по ключу из словаря data
    if value is None:
        return jsonify({"error": "Key not found."}), 404 #Если значение не найдено, возвращаем ошибку с кодом 404 (Not Found)

    return jsonify({"key": key, "value": value}), 200 #Если значение найдено, возвращаем его в формате JSON с кодом 200 (OK)

@limiter.limit("10 per minute", methods=["DELETE"])
@app.route("/delete/<key>", methods=["DELETE"])
def delete_key(key): #Определяем функцию delete_key, которая будет вызываться, когда поступит DELETE-запрос на указанный маршрут. 
    if key not in data: #Проверяем, существует ли ключ key в словаре data
        return jsonify({"error": "Key not found."}), 404

    del data[key] #Если ключ найден, удаляем его из словаря data
    save_data() #Вызываем функцию save_data, чтобы сохранить обновленные данные (без удаленного ключа) в файл data.json
    return jsonify({"message": "Key deleted successfully."}), 200

@app.route("/exists/<key>", methods=["GET"])
def key_exists(key): #Определяем функцию key_exists, которая будет вызываться, когда поступит GET-запрос на указанный маршрут. 
    exists = key in data #Проверяем, существует ли ключ key в словаре data. Результат (True или False) сохраняется в переменной exists
    return jsonify({"key": key, "exists": exists}), 200
#Возвращаем JSON-ответ, содержащий проверяемый ключ и его статус существования (True или False), с кодом 200 (OK)

if __name__ == "__main__":
    app.run(debug=True)
