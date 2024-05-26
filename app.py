from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Задание 1. Реализовать GET эндпоинт /number/, который принимает параметр запроса – param с числом. 
            # Вернуть рандомно сгенерированное число, умноженное на значение из параметра в формате JSON.


@app.route('/number/', methods=['GET'])
def get_number():

    param = request.args.get('param')

    if param is None:
        return jsonify({'error': 'Не задан параметр "param"'}), 400
    
    try:
        param = int(param) 
    except ValueError:
        return jsonify({'error': 'Параметр "param" должен быть числом'}), 400
    
    random_number = random.randint(1, 100)
    result = random_number * param
    return jsonify({'Результат': result})


# Задание 2. Реализовать POST эндпоинт /number/, который принимает в теле запроса JSON с полем jsonParam.
            # Вернуть сгенерировать рандомно число, умноженное на то, что пришло в JSON и рандомно выбрать операцию. 


@app.route('/number/', methods=['POST'])
def post_number():

    number = request.json
  
    if number is None or 'jsonParam' not in number:
        return jsonify({'error': 'Не задан параметр JSON "jsonParam"'}), 400
    
    try:
        json_param = int(number['jsonParam'])
    except ValueError:
        return jsonify({'error': 'Параметр JSON "jsonParam" должен быть числом'}), 400
    
    random_number = random.randint(0, 100)
 
    operations = ['Сложение', 'Вычитание', 'Умножение', 'Деление']
    operation = random.choice(operations)

    if operation == 'Сложение':
        result = random_number + json_param
    elif operation == 'Вычитание':
        result = random_number - json_param
    elif operation == 'Умножение':
        result = random_number * json_param
    else:
        if json_param == 0:
            return jsonify({'error': 'Нельзя делить на ноль'}), 400
        result = random_number / json_param
    
    return jsonify({'Результат': result, 'Выбранная операция': operation})


# Задание 3. Реализовать DELETE эндпоинт /number/, в ответе сгенерировать число и рандомную операцию.


@app.route('/number/', methods=['DELETE'])
def delete_number():

    random_number = random.randint(0, 100)
    operations = ['Сложение', 'Вычитание', 'Умножение', 'Деление']
    operation = random.choice(operations)
    json_param = random.randint(0, 100)
    
    if operation == 'Сложение':
        result = random_number + json_param
    elif operation == 'Вычитание':
        result = random_number - json_param
    elif operation == 'Умножение':
        result = random_number * json_param
    else:
        if json_param == 0:
            return jsonify({'error': 'Нельзя делить на ноль'}), 400
        result = random_number / json_param
    
    return jsonify({'Результат': result, 'Выбранная операция': operation})




