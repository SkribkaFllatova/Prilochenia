from flask import Flask, jsonify
import os  # Импортируем модуль os

app = Flask(__name__)

INSTANCE_ID = os.getenv('INSTANCE_ID', 'unknown')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "instance_id": INSTANCE_ID}), 200

@app.route('/process', methods=['GET'])
def process():
    return jsonify({"message": "Processed by instance", "instance_id": INSTANCE_ID}), 200

if __name__ == '__main__':
    port = int(os.getenv('FLASK_RUN_PORT', 5003))
    app.run(host='0.0.0.0', port=port)