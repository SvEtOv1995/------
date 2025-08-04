from flask import Flask, request, jsonify, send_from_directory
import os
import json
from datetime import datetime
import logging

app = Flask(__name__, static_folder='static')

# ✅ Включаем логирование всех запросов, как в dev-сервере
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    app.logger.info(f'{request.remote_addr} - GET /')
    return send_from_directory('static', 'index.html')

@app.route('/track', methods=['POST'])
def track():
    data = request.json
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "data": data
    }

    # лог в файл
    with open("track_log.txt", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    # ✅ Выводим событие в лог (именно в стандартный вывод — Render это покажет)
    print(f"[CLIENT ACTION] {json.dumps(log_entry, ensure_ascii=False)}")
    app.logger.info(f'{request.remote_addr} - POST /track')

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5600))
    app.run(host="0.0.0.0", port=port)
