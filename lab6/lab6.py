from flask import Flask, jsonify, request, render_template
import requests
import time
import threading

app = Flask(__name__)

# Список инстансов (предполагается, что они запущены локально)
instances = [
    {'ip': '127.0.0.1', 'port': 5001, 'status': 'active'},
    {'ip': '127.0.0.1', 'port': 5002, 'status': 'active'},
    {'ip': '127.0.0.1', 'port': 5003, 'status': 'active'}
]

# Индекс для стратегии Round Robin
round_robin_index = 0

def check_health():
    while True:
        for instance in instances:
            try:
                url = f"http://{instance['ip']}:{instance['port']}/health"
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    instance['status'] = 'active'
                else:
                    instance['status'] = 'inactive'
            except requests.exceptions.RequestException:
                instance['status'] = 'inactive'
        time.sleep(5)


threading.Thread(target=check_health, daemon=True).start() #Запускаем проверку состояния в отдельном потоке

@app.route('/health')
def health():
    return jsonify(instances) #Возвращает состояние всех инстансов

@app.route('/process')
def process():
    global round_robin_index #Перенаправляет запросы на активный инстанс по стратегии Round Robin

    for _ in range(len(instances)):
        instance = instances[round_robin_index]
        if instance['status'] == 'active':
            try:
                url = f"http://{instance['ip']}:{instance['port']}/process"
                response = requests.get(url, timeout=3)
                round_robin_index = (round_robin_index + 1) % len(instances)
                return response.text
            except requests.exceptions.RequestException:
                instance['status'] = 'inactive'

        round_robin_index = (round_robin_index + 1) % len(instances)

    return jsonify({"error": "No active instances available"}), 503

@app.route('/')
def home():
    return render_template('index.html', instances=instances) #Отображает Web UI с состоянием инстансов

@app.route('/add_instance', methods=['POST'])
def add_instance():
    ip = request.form['ip'] #Добавляет новый инстанс
    port = request.form['port']
    if not ip or not port.isdigit():
        return jsonify({"error": "Invalid IP or port"}), 400

    instances.append({'ip': ip, 'port': int(port), 'status': 'active'})
    return jsonify(instances)

@app.route('/remove_instance', methods=['POST'])
def remove_instance():
    index = int(request.form['index']) #Удаляет инстанс из пула по индексу
    if 0 <= index < len(instances):
        instances.pop(index)
        return jsonify(instances)
    return jsonify({"error": "Invalid index"}), 400

@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    global current_instance_index
    with lock:
        active_instances = [inst for inst in instances if inst['status'] == 'healthy']
        if not active_instances:
            return jsonify({"error": "Нет доступных экземпляров"}), 503
        instance = active_instances[current_instance_index % len(active_instances)]
        current_instance_index += 1

    target_url = f"http://{instance['ip']}:{instance['port']}/{path}"

    try:
        if request.method == 'GET':
            response = requests.get(target_url, params=request.args, timeout=5)
        elif request.method == 'POST':
            response = requests.post(target_url, json=request.json, timeout=5)
        return (response.content, response.status_code, response.headers.items())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Не удалось подключиться к экземпляру", "подробности": str(e)}), 503

if __name__ == '__main__':
    app.run(port=5000)
