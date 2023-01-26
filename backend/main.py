import bcrypt
from datetime import timedelta, datetime
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.associationproxy import association_proxy


# init
app = Flask(__name__)
app.config.from_object(__name__)
app.config["SECRET_KEY"] = "spos"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@127.0.0.1/spos"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["REMEMBER_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(seconds=30)      

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

CORS(
    app, 
    resources={r"/*":{'origins': "*"}},
    expose_headers=["Content-Type", "X-CSRFToken"],
    supports_credentials=True,
)

csrf = CSRFProtect(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

# app.config['CORS_HEADERS'] = 'Content-Type'
# CORS(app, resources={r"/*":{'origins': "*", "allow_headers": "Access-Control-Allow-Origin"}})
# header('Access-Control-Allow-Origin: *');
# header('Access-Control-Allow-Methods: GET, POST, PATCH, PUT, DELETE, OPTIONS');
# header('Access-Control-Allow-Headers: Origin, Content-Type, X-Auth-Token');
# CORS(app, resources={r"/*":{
#     'origins': "http://localhost:8080",
#     "allow_headers": "Access-Control-Allow-Origin"
#     }})



# secondary database models 
class CartProduct(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column("product_id", db.String(18), db.ForeignKey("product.id"), nullable=False)
    cart_id = db.Column("cart_id", db.String(18), db.ForeignKey("cart.id"), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Integer, nullable=False)

    product = db.relationship("Product", back_populates="cart_association")
    cart = db.relationship("Cart", back_populates="product_association")


class CategoryProduct(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column("product_id", db.String(18), db.ForeignKey("product.id"), nullable=False)
    category_id = db.Column("category_id", db.String(18), db.ForeignKey("category.id"), nullable=False)

    product = db.relationship("Product", back_populates="category_association")
    category = db.relationship("Category", back_populates="products")


class InvoiceProduct(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column("product_id", db.String(18), db.ForeignKey("product.id"), nullable=False)
    invoice_id = db.Column("invoice_id", db.String(18), db.ForeignKey("invoice.id"), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Integer, nullable=False)

    product = db.relationship("Product", back_populates="invoice_association")
    invoice = db.relationship("Invoice", back_populates="product_association")




# primary database models
class Admin(db.Model, UserMixin):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(9), nullable=False)

    # def __init__(self, aid, password):
    #     self.id = aid
    #     self.password = password


class Customer(db.Model, UserMixin):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(99), nullable=False, unique=True)
    password = db.Column(db.String(99), nullable=False)

    invoices = db.relationship("Invoice", backref="customer")               # for one to many relationship as the parent
    cart = db.relationship("Cart", backref="customer", uselist=False)       # for one to one relationship

    # def __init__(self, username, password):
    #     self.username = username
    #     self.password = password


class Product(db.Model, UserMixin):
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


class Category(db.Model, UserMixin):
    __tablename__ = "category"
    id = db.Column(db.String(18), primary_key=True)
    name = db.Column(db.String(27), nullable=False)

    products = db.relationship("CategoryProduct", back_populates="category")

    def __init__(self, name, cid="ctg-" + datetime.now().strftime("%Y%m%d%H%M%S")):
        self.id = cid
        self.name = name


class Cart(db.Model, UserMixin):
    __tablename__ = "cart"
    id = db.Column(db.String(18), primary_key=True)
    date = db.Column(db.String(27), nullable=False)
    total_qty = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    grand_price = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(9), db.ForeignKey("customer.username"))  # for one to one relationship

    # for many to many relationship
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


class Invoice(db.Model, UserMixin):
    __tablename__ = "invoice"
    id = db.Column(db.String(18), primary_key=True)
    date = db.Column(db.String(27), nullable=False)
    total_qty = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)                     
    username = db.Column(db.String(9), db.ForeignKey("customer.username"))  # for one to many relationship as the child

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
        postData = request.get_json()
        username = postData.get("username")
        theCart = Cart.query.filter_by(username=username).first()
        # theCart = postData
        theCart.date = postData.get("date")
        theCart.grand_price = postData.get("grand_price")
        theCart.price = postData.get("price")
        theCart.total_qty = postData.get("total_qty")
        db.session.commit()

        for cp in postData.get("product_association"):
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
        postData = request.get_json()
        # add new invoice
        newInvoice = Invoice(
            postData.get("date"), 
            postData.get("total_qty"),
            postData.get("total_price"),
            postData.get("username")
        )
        db.session.add(newInvoice)
        db.session.commit()
        # add its products
        for cp in postData.get("products"):
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




# user stuffs
@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))


@app.route("/getcsrf", methods=["GET"])
def get_csrf():
    token = generate_csrf()
    response = jsonify({"detail": "CSRF cookie set"})
    response.headers.set("X-CSRFToken", token)
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    response_object = {"status": "success"}
    if request.method == "POST":
        postData = request.get_json()
        username = postData.get("username")
        password = postData.get("password")

        # validate data login
        theCustomer = Customer.query.filter_by(username=username).first()
        if bcrypt.checkpw(password.encode(), theCustomer.password.encode()):
            # logging in and create a session
            login_user(theCustomer)
            response_object["message"] = "login success"
        else:
            response_object["status"] = "fail"
            response_object["message"] = "data login is not available"
    else:
        response_object["status"] = "fail"
        response_object["message"] = "request method is not accepted"
    return response_object


@app.route("/getsession", methods=["GET"])
def check_session():
    response_object = {"status": "success"}
    if current_user.is_authenticated:
        return response_object

    response_object["status"] = "fail"
    return response_object


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    response_object = {"status": "success"}

    # logging out the customer and remove the session
    logout_user()
    return response_object






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
        postData = request.get_json()
        newCart = Cart(
            postData.get("date"),
            postData.get("total_qty"),
            postData.get("discount"),
            postData.get("total_price"),
            postData.get("username")
        )
        db.session.add(newCart)
        db.session.commit()

        # carting
        relatedProduct = Product.query.filter_by(id=postData.get("products")[0]).first()
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
        adminA = Admin(password="pwAA")

        # add customers
        cusA = Customer(username="cusA", password=bcrypt.hashpw("pwCA".encode(), bcrypt.gensalt()))
        cusB = Customer(username="cusB", password=bcrypt.hashpw("pwCB".encode(), bcrypt.gensalt()))

        # execute primary data
        db.session.add_all([
            adminA, 
            cusA, cusB
        ])
        db.session.commit()
        print("1st added is succeed")

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
            cartA, cartB,
            prodA, prodB,
            ctgA, ctgB, ctgC, ctgD
        ])
        db.session.commit()
        print("2nd added is succeed")


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
        print("3rd added is succeed")

        response_object["message"] = "all data have been added"
    except:
        db.session.rollback()
        response_object["message"] = "all data have been added already"
    return jsonify(response_object)






if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)






# @app.route("/login", methods=["GET", "POST"])
# def login():
#     response_object = {"status": "success"}
#     if request.method == "POST":
#         if 'authKey' in session:
#             response_object["data"] = session['authKey'].decode()
#             response_object["message"] = "login success"
#         else:
#             postData = request.get_json()
#             username = postData.get("username")
#             password = postData.get("password")

#             # validate data login
#             theCustomer = Customer.query.filter_by(username=username).first()
#             if bcrypt.checkpw(password.encode(), theCustomer.password.encode()):
#                 # encrypt username
#                 encryptedUsername = bcrypt.hashpw(username.encode(), bcrypt.gensalt())
#                 print("ASDASD:",encryptedUsername)
#                 print("ASDASD:",encryptedUsername.decode())

#                 # create a session with encryptedPassword as the password
#                 # encryptedUsername == authKey
#                 session.permanent = True
#                 session['username'] = username
#                 session['authKey'] = encryptedUsername
#                 response_object["data"] = session['authKey'].decode()
#                 response_object["message"] = "login success"
#             else:
#                 response_object["status"] = "fail"
#                 response_object["message"] = "data login is not available"
#     else:
#         response_object["status"] = "fail"
#         response_object["message"] = "request is not accepted"
#     return response_object


# @app.route("/logout", methods=["GET", "POST"])
# def logout():
#     response_object = {"status": "success"}
#     session.pop("authKey", None)
#     session.pop("username", None)
#     if "authKey" in session or "username" in session:
#         response_object["status"] = "fail"
#         response_object["message"] = "logout is failed"
#     else:
#         response_object["message"] = "logout is succeed"
#     return response_object


# @app.route("/verAuth", methods=["GET", "POST"])
# def verAuth():
#     response_object = {"status": "success"}
#     if request.method == "POST":
#         if 'authKey' in session:
#             postData = request.get_json()
#             print("   ")
#             print(session["username"])
#             print(postData["frontKey"])
#             print(session["username"].encode())
#             print(postData["frontKey"].encode())
#             print("   ")
#             if bcrypt.checkpw(session["username"].encode(), postData["frontKey"].encode()):
#                 response_object["message"] = "auth key valid"
#             else:
#                 response_object["status"] = "fail"
#                 response_object["message"] = "auth key invalid"
#         else:
#             response_object["status"] = "fail"
#             response_object["message"] = "auth key has not yet added"
#     else:
#         response_object["status"] = "fail"
#         response_object["message"] = "request is not accepted"
#     return response_object









# references:
# https://www.youtube.com/watch?v=VVX7JIWx-ss&ab_channel=PrettyPrinted (one-to-many database relationship with flask-alchemy)
# https://www.youtube.com/watch?v=47i-jzrrIGQ&ab_channel=PrettyPrinted (many-to-many database relationship with flask-alchemy)
# https://www.youtube.com/watch?v=IlkVu_LWGys&ab_channel=PrettyPrinted (many-to-many database relationship with flask-alchemy, association cover)
# https://www.youtube.com/watch?v=JI76IvF9Lwg&ab_channel=PrettyPrinted (one-to-one database relationship with flask-alchemy)

# parameter descriptions:
# backref behaves as if create an additional column inside the table that has relationship with
# back_populates tells SqlAlchemy which column to link with when it joins the two tables
# associationproxy helps to simplify the process of accessing between two tables that have many to many relationship

# code reflections:
# I just realized that the implementation of using relationship is still solely for initiation, while for CRUD process, it turns out has not yet being used.
# for example, when create a new invoice, what I should do is to add also the backref inside of the initiation. 
# But for many to many relationship, it turns out I have implemented it!! 