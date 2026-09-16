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
        tie_number = player_sum
    elif player_sum > banker_sum:
        result = "player"
        tie_number = None
    else:
        result = "banker"
        tie_number = None

    return {
        "result": result,
        "player_sum": player_sum,
        "banker_sum": banker_sum,
        "tie_number": tie_number, # só vem número quando é tie
        "dices": [d1, d2, d3, d4],
        "player_dices": [d1, d2],
        "banker_dices": [d3, d4],
        "timestamp": int(time.time())
    }

@app.route('/')
def home():
    return jsonify({"status": "API com Tie + número funcionando"})

@app.route('/history')
def history_endpoint():
    if len(history) < 50:
        for _ in range(50):
            history.append(get_live_result())
    else:
        history.append(get_live_result())
        if len(history) > 500:
            history.pop(0)
    # Agora retorna "player" / "banker" / "tie-8" já com número
    simple = []
    for h in history[-100:]:
        if h["result"] == "tie":
            simple.append(f"tie-{h['tie_number']}")
        else:
            simple.append(h["result"])
    return jsonify(simple)

@app.route('/full')
def full():
    return jsonify(history[-100:])

@app.route('/latest')
def latest():
    data = get_live_result()
    history.append(data)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
