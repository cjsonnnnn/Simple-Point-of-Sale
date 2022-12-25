from flask import Flask, redirect, request, url_for, render_template, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from datetime import timedelta
from uuid import uuid4
from flask_cors import CORS
import json


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
ma = Marshmallow(app)


# create database models 
class Product(db.Model):
    __tablename__ = "product"
    product_id = db.Column(db.String(18), primary_key=True)
    name = db.Column(db.String(54), nullable=False)
    price = db.Column(db.String(200), nullable=False)
    img_link = db.Column(db.String(999), nullable=False)

    def __init__(self, name, price, img_link):
        self.product_id = "p-" + datetime.now().strftime("%Y%m%d%H%M%S")
        self.name = name
        self.price = price
        self.img_link = img_link


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_fk = True




@app.route("/lol")
def addProduct():
    # print("hello")
    # if request.method == "POST":
    #     newProduct = Product("sdakgsjdq", "sdakgsjdq", "sdakgsjdq", "sdakgsjdq")
    #     db.session.add(newProduct)
    #     db.session.commit()
    #     return "hai"
    # return jsonify({
    #     "hai": output
    # })
    return "hai"

@app.route("/getProduct", methods=["GET"])
def getProduct():
    product = Product.query.all()
    product_schema = ProductSchema(many=True)
    return product_schema.dump(product)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)