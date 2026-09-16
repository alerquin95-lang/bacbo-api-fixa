from flask import Flask, jsonify, request
from flask_cors import CORS
import os, json, time

app = Flask(__name__)
CORS(app)

HISTORY_FILE = "/tmp/bacbo_history.json"
PUSH_SECRET = os.getenv("PUSH_SECRET", "leonbet2026")  # troque no Render > Environment

history = []

if os.path.exists(HISTORY_FILE):
    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    except:
        history = []

def save_history():
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history[-500:], f)
    except Exception as e:
        print(f"Erro salvar: {e}")

@app.route('/')
def home():
    return jsonify({
        "status": "BAC BO API REAL - Leonbet Mode",
        "total": len(history),
        "mode": "Aguardando push do seu PC logado na Leonbet",
        "endpoints": ["/history", "/full", "/latest", "/push"]
    })

@app.route('/history')
def get_history():
    # NUNCA mais gera aleatório no F5
    out = []
    for h in history[-100:]:
        if h["result"] == "tie":
            out.append(f"tie-{h['player_sum']}")
        elif h["result"] == "player":
            out.append(f"player-{h['player_sum']}")
        else:
            out.append(f"banker-{h['banker_sum']}")
    return jsonify(out)

@app.route('/full')
def full():
    return jsonify(history[-100:])

@app.route('/latest')
def latest():
    if len(history) == 0:
        return jsonify({"status": "aguardando primeiro resultado real da Leonbet"})
    return jsonify(history[-1])

@app.route('/push', methods=['POST'])
def push():
    data = request.get_json()
    if not data:
        return jsonify({"error": "sem json"}), 400
    if data.get("secret") != PUSH_SECRET:
        return jsonify({"error": "secret errado"}), 401

    # esperado: result = player/banker/tie, player_sum, banker_sum
    try:
        h = {
            "result": data["result"],  # player, banker, tie
            "player_sum": int(data.get("player_sum", 0)),
            "banker_sum": int(data.get("banker_sum", 0)),
            "dices": data.get("dices", []),
            "timestamp": int(time.time())
        }
        # evita duplicar mesmo resultado seguido no mesmo segundo
        if len(history) > 0 and history[-1]["result"] == h["result"] and history[-1]["player_sum"] == h["player_sum"] and history[-1]["banker_sum"] == h["banker_sum"]:
            # se for igual ao último e com menos de 20s, ignora
            if int(time.time()) - history[-1]["timestamp"] < 20:
                return jsonify({"ok": False, "msg": "duplicado ignorado"})
        
        history.append(h)
        if len(history) > 500:
            history.pop(0)
        save_history()
        print(f"REAL PUSH: {h}")
        return jsonify({"ok": True, "total": len(history), "added": h})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
        history.append(get_live_result())
        if len(history) > 500:
            history.pop(0)

    final = []
    for h in history[-100:]:
        if h["result"] == "tie":
            final.append(f"tie-{h['player_sum']}")
        elif h["result"] == "player":
            final.append(f"player-{h['player_sum']}")
        else:
            final.append(f"banker-{h['banker_sum']}")
    return jsonify(final)

@app.route('/full')
def full():
    return jsonify(history[-100:])

@app.route('/latest')
def latest():
    data = get_live_result()
    history.append(data)
    # retorna já formatado com número
    if data["result"] == "tie":
        data["formatted"] = f"tie-{data['player_sum']}"
    elif data["result"] == "player":
        data["formatted"] = f"player-{data['player_sum']}"
    else:
        data["formatted"] = f"banker-{data['banker_sum']}"
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
