from flask import Flask, jsonify, request
import os, time, json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

FILE = "history.json"
SECRET = os.getenv("PUSH_SECRET", "leonbet2026")

def load_history():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(h):
    with open(FILE, "w") as f:
        json.dump(h[-500:], f)

history = load_history()

@app.route('/')
def home():
    return jsonify({"status":"OK", "total": len(history)})

@app.route('/history')
def hist():
    # formato que seu app já entende
    out=[]
    for h in history[-100:]:
        if h["result"]=="tie":
            out.append(f"tie-{h['player_sum']}")
        elif h["result"]=="player":
            out.append(f"player-{h['player_sum']}")
        else:
            out.append(f"banker-{h['banker_sum']}")
    return jsonify(out)

@app.route('/full')
def full():
    return jsonify(history[-100:])

@app.route('/push', methods=['POST'])
def push():
    data = request.get_json()
    if data.get("secret") != SECRET:
        return jsonify({"error":"secret errado"}), 401
    
    h = {
        "result": data["result"],
        "player_sum": int(data["player_sum"]),
        "banker_sum": int(data["banker_sum"]),
        "timestamp": int(time.time())
    }
    # evita duplicado
    if history and history[-1]["timestamp"] == h["timestamp"] and history[-1]["result"] == h["result"]:
        return jsonify({"ok": True, "duplicated": True})

    history.append(h)
    save_history(history)
    print(f"NOVO RESULTADO REAL: {h}")
    return jsonify({"ok": True, "total": len(history)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
