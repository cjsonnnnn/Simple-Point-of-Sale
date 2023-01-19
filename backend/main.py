from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from flask_cors import CORS


# init
app = Flask(__name__)
app.config.from_object(__name__)
app.config["SECRET_KEY"] = "spos"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@127.0.0.1/spos"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app, resources={r"/*":{'origins': "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'
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




# secondary database models 
class CartProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column("product_id", db.String(18), db.ForeignKey("product.id"), nullable=False)
    cart_id = db.Column("cart_id", db.String(18), db.ForeignKey("cart.id"), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Integer, nullable=False)

    product = db.relationship("Product", back_populates="cart_association")
    cart = db.relationship("Cart", back_populates="product_association")


class CategoryProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column("product_id", db.String(18), db.ForeignKey("product.id"), nullable=False)
    category_id = db.Column("category_id", db.String(18), db.ForeignKey("category.id"), nullable=False)

    product = db.relationship("Product", back_populates="category_association")
    category = db.relationship("Category", back_populates="products")



class InvoiceProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column("product_id", db.String(18), db.ForeignKey("product.id"), nullable=False)
    invoice_id = db.Column("invoice_id", db.String(18), db.ForeignKey("invoice.id"), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Integer, nullable=False)

    product = db.relationship("Product", back_populates="invoice_association")
    invoice = db.relationship("Invoice", back_populates="product_association")




# primary database models
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.String(9), primary_key=True)
    password = db.Column(db.String(9), nullable=False)

    def __init__(self, aid, password):
        self.id = aid
        self.password = password


class Customer(db.Model):
    __tablename__ = "customer"
    username = db.Column(db.String(9), primary_key=True)
    password = db.Column(db.String(9), nullable=False)
    invoices = db.relationship("Invoice", backref="customer")
    cart = db.relationship("Cart", backref="customer", uselist=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.String(18), primary_key=True)
    name = db.Column(db.String(54), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img_link = db.Column(db.String(999), nullable=False)

    cart_association = db.relationship("CartProduct", back_populates="product")
    carts = association_proxy("cart_association", "cart")

    category_association = db.relationship("CategoryProduct", back_populates="product")
    categories = association_proxy("category_association", "category")

    invoice_association = db.relationship("InvoiceProduct", back_populates="product")
    invoices = association_proxy("invoice_association", "invoice")

    def __init__(self, name, price, img_link, pid="prd-" + datetime.now().strftime("%m%d%H%M%S")):
        self.id = pid
        self.name = name
        self.price = price
        self.img_link = img_link


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.String(18), primary_key=True)
    name = db.Column(db.String(27), nullable=False)

    products = db.relationship("CategoryProduct", back_populates="category")

    def __init__(self, name, cid="ctg-" + datetime.now().strftime("%Y%m%d%H%M%S")):
        self.id = cid
        self.name = name


class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.String(18), primary_key=True)
    date = db.Column(db.String(27), nullable=False)
    total_qty = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    grand_price = db.Column(db.Integer, nullable=False)

    username = db.Column(db.String(9), db.ForeignKey("customer.username"))

    product_association = db.relationship("CartProduct", back_populates="cart")
    products = association_proxy("product_association", "product")

    def __init__(self, date, total_qty, discount, price, grand_price, username, cid="ca-" + datetime.now().strftime("%m%d%H%M%S%f")[:-3]):
        self.id = cid
        self.date = date
        self.total_qty = total_qty
        self.discount = discount
        self.price = price
        self.grand_price = grand_price
        self.username = username


class Invoice(db.Model):
    __tablename__ = "invoice"
    id = db.Column(db.String(18), primary_key=True)
    date = db.Column(db.String(27), nullable=False)
    total_qty = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)

    username = db.Column(db.String(9), db.ForeignKey("customer.username"))

    product_association = db.relationship("InvoiceProduct", back_populates="invoice")
    products = association_proxy("product_association", "product")

    def __init__(self, date, total_qty, total_price, username, iId="inv-" + datetime.now().strftime("%m%d%H%M%S%f")[:-3]):
        self.id = iId
        self.date = date
        self.total_qty = total_qty
        self.total_price = total_price
        self.username = username






# database schemes
class CartProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CartProduct
        include_fk = True

class CategoryProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CategoryProduct
        include_fk = True

class InvoiceProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = InvoiceProduct
        include_fk = True

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        include_fk = True

class AdminSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Admin
        include_fk = True

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        include_fk = True

class ProductSchema(ma.SQLAlchemyAutoSchema):
    categories = ma.Nested(CategorySchema, many=True)
    class Meta:
        model = Product
        include_fk = True

class CartSchema(ma.SQLAlchemyAutoSchema):
    product_association = ma.Nested(CartProductSchema, many=True)
    class Meta:
        model = Cart
        include_fk = True

class InvoiceSchema(ma.SQLAlchemyAutoSchema):
    product_association = ma.Nested(InvoiceProductSchema, many=True)
    class Meta:
        model = Invoice
        include_fk = True



# get
@app.route("/getProducts", methods=["GET"])
def getProducts():
    product = Product.query.all()
    product_schema = ProductSchema(many=True)
    return product_schema.dump(product)


@app.route("/getAllCategories", methods=["GET"])
def getAllCategories():
    cAll = Category.query.all()
    category_schema = CategorySchema(many=True)
    return category_schema.dump(cAll)


@app.route("/getCart/<username>", methods=["GET"])
def getCart(username):
    cCart = Cart.query.filter_by(username=username).all()
    cart_schema = CartSchema(many=True)
    return cart_schema.dump(cCart)


@app.route("/addCartProduct/<username>&<pId>", methods=["GET"])
def addCartProduct(username, pId):
    response_object  = {"status": "success"}
    theCart = Cart.query.filter_by(username=username).first()
    theProduct = Product.query.filter_by(id=pId).first()
    initPrice = theProduct.price

    # appending / subcribing
    theCP = CartProduct(product=theProduct, cart=theCart, qty=1, subtotal=initPrice)
    db.session.add(theCP)
    db.session.commit()
    return jsonify(response_object)


@app.route("/removeCartProduct/<username>&<pId>", methods=["GET"])
def removeCartProduct(username, pId):
    response_object  = {"status": "success"}
    cartId = Cart.query.filter_by(username=username).first().id
    theCartProduct = CartProduct.query.filter_by(cart_id=cartId, product_id=pId).first()

    # removing / unsubcribing
    db.session.delete(theCartProduct)
    db.session.commit()
    return jsonify(response_object)


@app.route("/updateCart", methods=["GET", "POST"])
def updateCart():
    response_object  = {"status": "success"}
    if request.method == "POST":
        post_data = request.get_json()
        username = post_data.get("username")
        theCart = Cart.query.filter_by(username=username).first()
        # theCart = post_data
        theCart.date = post_data.get("date")
        theCart.grand_price = post_data.get("grand_price")
        theCart.price = post_data.get("price")
        theCart.total_qty = post_data.get("total_qty")
        db.session.commit()

        for cp in post_data.get("product_association"):
            theCP = CartProduct.query.filter_by(cart_id=cp["cart_id"], product_id=cp["product_id"]).first()
            theCP.qty = cp["qty"]
            theCP.subtotal = cp["subtotal"]
            db.session.commit()

        response_object["message"] = "cart updated"
    else:
        response_object["message"] = "cart failed to update"
    return jsonify(response_object)


@app.route("/resetCart/<username>", methods=["GET"])
def resetCart(username):
    response_object  = {"status": "success"}
    uCart = Cart.query.filter_by(username=username).first()
    uCart.total_qty = 0
    uCart.price = 0
    uCart.grand_price = 0
    db.session.commit()

    for cp in uCart.product_association:
        db.session.delete(cp)
        db.session.commit()
    return jsonify(response_object)


@app.route("/addInvoice", methods=["GET", "POST"])
def addInvoice():
    response_object = {"status": "success"}
    if request.method == "POST":
        post_data = request.get_json()
        # add new invoice
        newInvoice = Invoice(
            post_data.get("date"), 
            post_data.get("total_qty"),
            post_data.get("total_price"),
            post_data.get("username")
        )
        db.session.add(newInvoice)
        db.session.commit()
        # add its products
        for cp in post_data.get("products"):
            theProduct = Product.query.filter_by(id=cp["product_id"]).first()
            theIP = InvoiceProduct(product=theProduct, invoice=newInvoice, qty=cp["qty"], subtotal=cp["subtotal"])
            db.session.add(theIP)
            db.session.commit()

        response_object["message"] = "new invoice added"
    else:
        response_object["message"] = "new invoice failed to add"
    return response_object


@app.route("/getInvoice/<username>", methods=["GET"])
def getInvoice(username):
    cInv = Invoice.query.filter_by(username=username).all()
    invoice_schema = InvoiceSchema(many=True)
    return invoice_schema.dump(cInv)



@app.route("/experiment")
def testing():
    response_object  = {"status": "success"}
    
    theCart = Cart.query.filter_by(id="ca-1").first()
    theProduct = Product.query.filter_by(id="prd-1").first()
    theCartProduct = CartProduct.query.filter_by(product_id="prd-1", cart_id="ca-1").first()

    cartsch = CartSchema()
    prdsch = ProductSchema()
    cpsch = CartProductSchema()
    
    # response_object["hei"] = select(CartProduct).where(Product.id=="prd-1" AND Cart.id=="ca-1")

    # db.session.delete(theCartProduct)
    # db.session.commit()

    response_object["sda"] = theCart.product_association[0].cart_id

    # return cpsch.dump(theCartProduct)
    return jsonify(response_object)




# post
# @cross_origin(origin='*', headers=['content-type'])
@app.route("/addCart", methods=["GET", "POST"])
def addCart():
    response_object  = {"status": "success"}
    if request.method == "POST":
        post_data = request.get_json()
        newCart = Cart(
            post_data.get("date"),
            post_data.get("total_qty"),
            post_data.get("discount"),
            post_data.get("total_price"),
            post_data.get("username")
        )
        db.session.add(newCart)
        db.session.commit()

        # carting
        relatedProduct = Product.query.filter_by(id=post_data.get("products")[0]).first()
        relatedProduct.carting.append(newCart)
        db.session.commit()

        response_object["message"] = "new cart added"
    else:
        response_object["message"] = "new cart failed to add"
    return jsonify(response_object)


@app.route("/")
def InitializeData():
    response_object = {"status": "success"}
    try:
        # add an admin
        adminA = Admin("admA", "pwAA")

        # add customers
        cusA = Customer("cusA", "pwCA")
        cusB = Customer("cusB", "pwCB")

        # add their (customers) carts
        cartA = Cart(datetime.now().strftime("%Y%m%d%H%M%S"), 0, 36, 0, 0, "cusA", cid="ca-1")
        cartB = Cart(datetime.now().strftime("%Y%m%d%H%M%S"), 0, 36, 0, 0, "cusB", cid="ca-2")

        # add products
        prodA = Product("Sony X1", 2700000, "https://tinyurl.com/h5mzuukd", "prd-1")
        prodB = Product("Shure Microphone", 1800000, "https://tinyurl.com/mr36xp8h", "prd-2")

        # add categories
        ctgA = Category("Technology", "ctg-1")
        ctgB = Category("Camera", "ctg-2")
        ctgC = Category("Microphone", "ctg-3")
        ctgD = Category("Guitar", "ctg-4")
        # ctgE = Category("Music Instrument", "ctg-5")
        # ctgF = Category("Computer", "ctg-6")
        # ctgG = Category("Drum", "ctg-7")

        # execute primary data
        db.session.add_all([
            adminA, 
            cusA, cusB, 
            cartA, cartB,
            prodA, prodB,
            ctgA, ctgB, ctgC, ctgD
        ])
        db.session.commit()


        # add their (products) categories
        pcA = CategoryProduct(product=prodA, category=ctgA)
        pcB = CategoryProduct(product=prodA, category=ctgB)
        pcC = CategoryProduct(product=prodB, category=ctgA)
        pcD = CategoryProduct(product=prodB, category=ctgC)

        # execute secondary data
        db.session.add_all([
            pcA, pcB, pcC, pcD
        ])
        db.session.commit()

        response_object["message"] = "all data have been added"
    except:
        db.session.rollback()
        response_object["message"] = "all data have been added already"
    return jsonify(response_object)






if __name__ == "__main__":
    with app.app_context():
        db.create_all()


    app.run(debug=True)









# references:
# https://www.youtube.com/watch?v=VVX7JIWx-ss&ab_channel=PrettyPrinted (one-to-many database relationship with flask-alchemy)
# https://www.youtube.com/watch?v=47i-jzrrIGQ&ab_channel=PrettyPrinted (many-to-many database relationship with flask-alchemy)
# https://www.youtube.com/watch?v=JI76IvF9Lwg&ab_channel=PrettyPrinted (one-to-one database relationship with flask-alchemy)