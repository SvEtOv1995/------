from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import os
import json

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/track', methods=['POST'])
def track():
    data = request.json
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "data": data
    }

    # Запись в файл
    with open("track_log.txt", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    print(f"[LOG] {log_entry}")
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5600))
    app.run(debug=False, host='0.0.0.0', port=port)
