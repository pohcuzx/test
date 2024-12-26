from flask import Flask, request, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)

# Đường dẫn đến file JSON
KEY_FILE = "server_keys.json"

def load_keys():
    if os.path.exists(KEY_FILE):
        try:
            with open(KEY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

@app.route('/verify', methods=['POST'])
def verify_key():
    data = request.get_json()
    key = data.get('key', '').strip()
    
    keys = load_keys()
    if key in keys:
        expiry = keys[key]
        try:
            exp_date = datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S")
            if exp_date > datetime.now():
                return jsonify({"valid": True, "expiry": expiry})
        except:
            pass
    return jsonify({"valid": False})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000))) 