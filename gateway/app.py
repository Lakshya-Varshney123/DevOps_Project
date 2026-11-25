import os, requests
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)
CATALOG = os.getenv("CATALOG_URL", "http://localhost:5001")
ORDERS = os.getenv("ORDER_URL", "http://localhost:5002")

@app.get("/")
def home(): return render_template("index.html")

@app.get("/health")
def health(): return jsonify(status="healthy", service="gateway")

@app.get("/api/menu")
def menu():
    try:
        r = requests.get(CATALOG + "/menu", timeout=5)
        return (r.text, r.status_code, {"Content-Type": "application/json"})
    except requests.RequestException:
        return jsonify(error="Catalog service unavailable"), 503

@app.route("/api/orders", methods=["GET", "POST"])
def orders():
    try:
        if request.method == "POST":
            r = requests.post(ORDERS + "/orders", json=request.get_json(silent=True) or {}, timeout=15)
        else:
            r = requests.get(ORDERS + "/orders", timeout=5)
        return (r.text, r.status_code, {"Content-Type": "application/json"})
    except requests.RequestException:
        return jsonify(error="Order service unavailable"), 503

if __name__ == "__main__": app.run(host="0.0.0.0", port=5000)
