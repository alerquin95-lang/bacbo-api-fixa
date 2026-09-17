from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # LIBERA TUDO

historico = []

@app.route('/')
def home():
    return 'API Bac Bo ON - CORS liberado'

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(historico)

@app.route('/history', methods=['POST'])
def add_history():
    data = request.get_json(force=True)
    print(f"Recebido: {data}")
    historico.append(data)
    if len(historico) > 500:
        historico.pop(0)
    return jsonify({"ok": True, "total": len(historico)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
