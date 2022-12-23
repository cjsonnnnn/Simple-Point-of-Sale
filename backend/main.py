from flask import Flask, redirect, request, url_for, render_template, session, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import timedelta
from uuid import uuid4
from flask_cors import CORS


# init
app = Flask(__name__)
app.config.from_object(__name__)
app.config["SECRET_KEY"] = "spos"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@127.0.0.1/spos"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app, resources={r"/*":{'origins': "*"}})
# CORS(app, resources={r"/*":{'origins': "*", "allow_headers": "Access-Control-Allow-Origin"}})
# header('Access-Control-Allow-Origin: *');
# header('Access-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS');
# header('Access-Control-Allow-Headers: Origin, Content-Type, X-Auth-Token');
# CORS(app, resources={r"/*":{
#     'origins': "http://localhost:8080",
#     "allow_headers": "Access-Control-Allow-Origin"
#     }})


db = SQLAlchemy(app)


# create database models 
class Product(db.Model):
    __tablename__ = "product"
    product_id = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    qty = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), unique=True, nullable=False)

    def __init__(self, name, qty, price, category):
        self.product_id = "p-" + datetime.now().strftime("%Y%m%d%H%M%S")
        self.name = name
        self.qty = qty
        self.price = price
        self.category = category
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)




@app.route("/addP", methods=["GET", "POST"])
def addProduct():
    print("hello")
    if request.method == "POST":
        newProduct = Product("sdakgsjdq", "sdakgsjdq", "sdakgsjdq", "sdakgsjdq")
        db.session.add(newProduct)
        db.session.commit()
        return "hai"

@app.route("/getProduct", methods=["GET"])
def getProduct():
    product = Product.query.filter_by(product_id="p-20221223031544").first()
    return product.toJSON()



if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)