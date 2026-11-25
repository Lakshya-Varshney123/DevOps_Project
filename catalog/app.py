from flask import Flask, jsonify
import os
app=Flask(__name__)
MENU=[
{"id":1,"name":"Margherita Pizza","description":"Tomato, mozzarella and basil.","price":249},
{"id":2,"name":"Veggie Burger","description":"Crispy vegetable patty with lettuce.","price":159},
{"id":3,"name":"Paneer Wrap","description":"Spiced paneer with crunchy vegetables.","price":189},
{"id":4,"name":"Masala Fries","description":"Golden fries tossed in house spices.","price":99},
{"id":5,"name":"Chocolate Brownie","description":"Rich chocolate brownie.","price":119},
{"id":6,"name":"Cold Coffee","description":"Chilled creamy coffee.","price":129}]
@app.get("/health")
def health(): return jsonify(status="healthy",service="catalog")
@app.get("/menu")
def menu(): return jsonify(MENU)
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.getenv("PORT","5001")))
