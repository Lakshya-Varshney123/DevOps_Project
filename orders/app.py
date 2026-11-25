import os, json, sqlite3, requests
from flask import Flask, jsonify, request
app=Flask(__name__)
DB="/data/orders.db"
CATALOG=os.getenv("CATALOG_URL","http://catalog:5001")
PAYMENT=os.getenv("PAYMENT_URL","http://payments:5003")
NOTIFY=os.getenv("NOTIFICATION_URL","http://notifications:5004")
def db():
    os.makedirs("/data",exist_ok=True); c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init():
    with db() as c: c.execute("CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT,customer TEXT,address TEXT,items TEXT,total REAL,status TEXT,payment_status TEXT)")
@app.get("/health")
def health(): return jsonify(status="healthy",service="orders")
@app.get("/orders")
def list_orders():
    with db() as c: rows=c.execute("SELECT * FROM orders ORDER BY id").fetchall()
    return jsonify([dict(r,items=json.loads(r["items"])) for r in rows])
@app.post("/orders")
def create():
    d=request.get_json(silent=True) or {}; customer=str(d.get("customer","")).strip(); address=str(d.get("address","")).strip(); entries=d.get("items")
    if not customer or not address or not isinstance(entries,list) or not entries: return jsonify(error="Customer, address and at least one item are required"),400
    try:
        mr=requests.get(CATALOG+"/menu",timeout=5); mr.raise_for_status(); menu={x["id"]:x for x in mr.json()}
    except requests.RequestException: return jsonify(error="Catalog service unavailable"),503
    normalized=[]; total=0
    for e in entries:
        try: iid=int(e["id"]); qty=int(e["quantity"])
        except (KeyError,TypeError,ValueError): return jsonify(error="Invalid item details"),400
        if iid not in menu or qty<1 or qty>20: return jsonify(error="Invalid menu item or quantity (1–20)"),400
        item=menu[iid]; subtotal=item["price"]*qty; total+=subtotal
        normalized.append({"id":iid,"name":item["name"],"quantity":qty,"subtotal":subtotal})
    try:
        pr=requests.post(PAYMENT+"/payments",json={"amount":total,"customer":customer},timeout=5); pr.raise_for_status(); payment=pr.json()
    except requests.RequestException: return jsonify(error="Payment service unavailable"),503
    if payment.get("status")!="authorized": return jsonify(error="Payment not authorized"),402
    with db() as c:
        cur=c.execute("INSERT INTO orders(customer,address,items,total,status,payment_status) VALUES(?,?,?,?,?,?)",(customer,address,json.dumps(normalized),total,"Confirmed",payment["status"])); oid=cur.lastrowid
    try: requests.post(NOTIFY+"/notifications",json={"order_id":oid,"customer":customer,"message":f"Your order #{oid} is confirmed."},timeout=3)
    except requests.RequestException: app.logger.warning("Notification unavailable for order %s",oid)
    return jsonify(id=oid,customer=customer,address=address,items=normalized,total=total,status="Confirmed",payment_status=payment["status"]),201
if __name__=="__main__":
    init(); app.run(host="0.0.0.0",port=int(os.getenv("PORT","5002")))
