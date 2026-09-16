from flask import Flask, jsonify
from flask_cors import CORS
import time
import random

app = Flask(__name__)
CORS(app)

# Memoria simples - guarda ultimos 500 resultados
history = []

# Simulador que funciona como se fosse Bac Bo real
# Quando quiser plugar scraper real, troca essa funcao
def get_live_result():
    # Aqui entraria o scraper real de CasinoScores/Bet365
    # Por enquanto gera resultado no formato real pra testar seu app
    result = random.choice(["player", "banker", "tie"])
    return {
        "result": result,
        "timestamp": int(time.time()),
        "dices": [random.randint(1,6), random.randint(1,6), random.randint(1,6), random.randint(1,6)]
    }

@app.route('/')
def home():
    return jsonify({
        "status": "Bac Bo API funcionando",
        "endpoints": ["/history", "/latest"],
        "aviso": "Scraping pode violar termos do site original. Use por sua conta e risco."
    })

@app.route('/history')
def history_endpoint():
    # Se historico vazio, gera 50
    if len(history) < 50:
        for _ in range(50):
            history.append(get_live_result())
    else:
        # Adiciona 1 novo a cada chamada (simula segunda tela)
        history.append(get_live_result())
        if len(history) > 500:
            history.pop(0)
    
    # Retorna so o array de resultados como o original fazia: ["player","banker","tie"...]
    simple = [h["result"] for h in history[-100:]]
    return jsonify(simple)

@app.route('/latest')
def latest():
    data = get_live_result()
    history.append(data)
    return jsonify(data)

@app.route('/full')
def full():
    return jsonify(history[-100:])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
