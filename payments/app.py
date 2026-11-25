from flask import Flask, jsonify, request
import os
app=Flask(__name__)
@app.get("/health")
def health(): return jsonify(status="healthy",service="payments")
@app.post("/payments")
def pay():
    d=request.get_json(silent=True) or {}
    try: amount=float(d.get("amount",0))
    except (TypeError,ValueError): return jsonify(error="Invalid amount"),400
    if amount<=0: return jsonify(error="Amount must be positive"),400
    # Demo-only authorization. No card data or real money is processed.
    return jsonify(status="authorized",transaction_id="DEMO-PAYMENT",amount=amount)
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.getenv("PORT","5003")))
