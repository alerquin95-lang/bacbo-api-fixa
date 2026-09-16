from flask import Flask, jsonify, request
import os, time
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
history=[]
SECRET=os.getenv("PUSH_SECRET","leonbet2026")

@app.route('/')
def home():
    return jsonify({"status":"OK"})

@app.route('/history')
def hist():
    return jsonify(history)

@app.route('/full')
def full():
    return jsonify(history)

@app.route('/push', methods=['POST'])
def push():
    data=request.get_json()
    if data.get("secret")!=SECRET:
        return jsonify({"error":"secret"}),401
    h={"result":data["result"],"player_sum":int(data["player_sum"]),"banker_sum":int(data["banker_sum"]),"timestamp":int(time.time())}
    history.append(h)
    return jsonify({"ok":True})

if __name__=='__main__':
    app.run(host='0.0.0.0', port=10000)
