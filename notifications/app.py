from flask import Flask, jsonify, request
from datetime import datetime, timezone
import os
app=Flask(__name__); messages=[]
@app.get("/health")
def health(): return jsonify(status="healthy",service="notifications")
@app.post("/notifications")
def notify():
    d=request.get_json(silent=True) or {}
    if not d.get("order_id") or not d.get("message"): return jsonify(error="order_id and message required"),400
    item={"order_id":d["order_id"],"customer":d.get("customer",""),"message":d["message"],"created_at":datetime.now(timezone.utc).isoformat()}
    messages.append(item); app.logger.info("Demo notification: %s",item)
    return jsonify(status="recorded",notification=item),201
@app.get("/notifications")
def list_notifications(): return jsonify(messages)
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.getenv("PORT","5004")))
