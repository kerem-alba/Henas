from flask import Flask, jsonify
from run_algorithm import run_algorithm  # run_algorithm'i içe aktar

app = Flask(__name__)

@app.route('/run', methods=['GET','POST'])

def run_hill_climbing_endpoint():
    try:
        result = run_algorithm()
        return jsonify({"status": "success", "result": result})  # Sonucu döndür
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
