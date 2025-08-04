from flask import Flask, request, jsonify, send_from_directory
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/track', methods=['POST'])
def track():
    data = request.json
    with open("track_log.txt", "a", encoding="utf-8") as f:
        f.write(json.dumps({"timestamp": datetime.utcnow().isoformat(), "data": data}, ensure_ascii=False) + "\n")
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5600))
    app.run(host="0.0.0.0", port=port)
