from flask import Flask, jsonify
from flask_cors import CORS
import time
import random

app = Flask(__name__)
CORS(app)

history = []

def get_live_result():
    d1, d2, d3, d4 = [random.randint(1,6) for _ in range(4)]
    player_sum = d1 + d2
    banker_sum = d3 + d4

    if player_sum == banker_sum:
        result = "tie"
    elif player_sum > banker_sum:
        result = "player"
    else:
        result = "banker"

    return {
        "result": result,
        "player_sum": player_sum,
        "banker_sum": banker_sum,
        "dices": [d1, d2, d3, d4],
        "timestamp": int(time.time())
    }

@app.route('/history')
def history_endpoint():
    if len(history) < 50:
        for _ in range(50):
            history.append(get_live_result())
    else:
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
