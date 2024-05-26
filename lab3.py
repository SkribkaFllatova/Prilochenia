import requests
import random  

def convert_operations(operation): 
    if operation == 'сложение':  
        return '+'  
    elif operation == 'вычитание':  
        return '-'  
    elif operation == 'умножение':  
        return '*' 
    elif operation == 'деление':  
        return '/'  
    else: 
        return None  


# Задание 1. Отправить запрос GET /number с параметром запроса param=[рандомное число от 1 до 10]. 
            # В ответ будет выдано число и операция - запомнить их. 


param_get = random.randint(1, 10)  
response_get = requests.get(f'http://127.0.0.1:5000/number/?param={param_get}')  
data_get = response_get.json()  
print("GET запрос - ", data_get)  
number_get = data_get.get('Результат', None)  
operation_get = data_get.get('Операция', None)      
print(f"GET запрос - Число={number_get}, Операция={operation_get}")  

operation_get = convert_operations(operation_get) 
# Задание 2. Отправить запрос POST /number с телом JSON {"jsonParam": [рандомное число от 1 до 10]}. 
            # В заголовках необходимо указать content-type=application/json. В ответ будет выдано число и операция - запомнить их. 


param_post = random.randint(1, 10)  
headers = {'Content-Type': 'application/json'}  
data_post = {'jsonParam': param_post} 
response_post = requests.post('http://127.0.0.1:5000/number/', json=data_post, headers=headers)
data_post = response_post.json()  
print("POST запрос - ", data_post)  
number_post = data_post.get('Результат', None)  
operation_post = data_post.get('Операция', None)  
print(f"POST запрос - Число={number_post}, Операция={operation_post}")


operation_post = convert_operations(operation_post)  
# Задание 3. Отправить запрос DELETE /number/. В ответ будет выдано число и операция - запомнить их. 


response_delete = requests.delete('http://127.0.0.1:5000/number/') 
data_delete = response_delete.json() 
print("DELETE запрос - ", data_delete)  
number_delete = data_delete.get('Результат', None) 
operation_delete = data_delete.get('Операция', None)  
print(f"DELETE запрос - Число={number_delete}, Операция={operation_delete}")


operation_delete = convert_operations(operation_delete) 
# Задание 4. Из полученных ответов составить выражение, посчитать и привести полученное значение к int(). 
            # Операции выполнять последовательно. Результат записать в отчет.


values = [number_get, number_post, number_delete] 

operations = [operation_get, operation_post, operation_delete]  

expression_parts = [] 
for values1, operations1 in zip(values, operations):  
    if operations1:  
        expression_parts.extend([str(values1), operations1]) 

expression_parts.append(str(values[-1]))  

expression = ' '.join(expression_parts)  

try:
    result = int(eval(expression))  
    print(f"Результат выражения {expression} = {result}")  
except Exception as expression_parts: 
    print("Возникла ошибка при вычислении", expression_parts) 