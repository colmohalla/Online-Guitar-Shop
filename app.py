from flask import Flask, render_template, session, redirect, url_for, g, request, make_response
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm, BuildForm, CheckoutForm, AdminForm, StockForm, QuoteForm
from functools import wraps

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "this-is-my-secret-key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


"""
My system has two kinds of user: regular ones, and administrators.
Choose Register on the main page in order to register as a regular user.
But to login as an administrator, go to Admin. the user name is hello and the password is world

"""

### User and Admin Required ###
@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id", None)
    g.admin = session.get("admin_id", None)
   
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect( url_for("login", next=request.url))
        return view(**kwargs)
    return wrapped_view

def admin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return redirect( url_for("admin", next=request.url))
        return view(**kwargs)
    return wrapped_view

### Index ###
@app.route("/")
def index():
    return render_template("index.html")


### Register User ###
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        password2 = form.password2.data
        db = get_db()
        possible_clashing_user = db.execute("""SELECT * FROM users
                                    WHERE user_id = ?""",(user_id,)).fetchone()
        if possible_clashing_user is not None:
            form.user_id.errors.append("User id already taken!")
        else:
            db.execute("""INSERT INTO users (user_id, password)
                                    VALUES (?,?);""",
                                    (user_id, generate_password_hash(password)))
            db.commit()
            return redirect( url_for("login") )
    return render_template("register.html", form=form)


### User Login ###
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        matching_user = db.execute("""SELECT * FROM users
                                    WHERE user_id = ?""",(user_id,)).fetchone()
        if matching_user is None:
            form.user_id.errors.append("Unknown user id!")
        elif not check_password_hash(matching_user["password"], password):
            form.password.errors.append("Incorrect password!")
        else:
            session.clear()
            session["user_id"] = user_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("index")
            return redirect(next_page)
    return render_template("login.html", form=form)


### View Guitars ###
@app.route("/guitars")
def guitars():
    db = get_db()
    guitars = db.execute("""SELECT * FROM guitars;""").fetchall()
    return render_template("guitars.html", guitars=guitars)


### View Individual Guitar ###
@app.route("/guitar/<int:guitar_id>") # individual guitar
def guitar(guitar_id):
    db = get_db()
    guitar = db.execute("""SELECT * FROM guitars
                            WHERE guitar_id = ?;""", (guitar_id,)).fetchone()
    return render_template("guitar.html", guitar=guitar)


### Add to Cart ###
@app.route("/add_to_cart/<int:guitar_id>")
@login_required
def add_to_cart(guitar_id):
    if "cart" not in session:   
        session["cart"] = {}    
    if guitar_id not in session["cart"]:    
        session["cart"][guitar_id] = 0  
    session["cart"][guitar_id] = session["cart"][guitar_id] + 1 
    return redirect( url_for("cart") )

### View Cart ###
@app.route("/cart")
@login_required
def cart():
    if "cart" not in session:  
        session["cart"] = {}
    names = {}
    prices = {}
    total = 0
    price = 0
    db = get_db()
    for guitar_id in session["cart"]:
        guitar = db.execute("""SELECT * FROM guitars
                                WHERE guitar_id = ?;""", (guitar_id,)).fetchone()
        name = guitar["name"]
        names[guitar_id] = name
        price = guitar["price"]
        prices[guitar_id] = price
        quantity = session["cart"][guitar_id] * guitar["price"]
        total += quantity
    return render_template("cart.html", cart=session["cart"], names=names, price=price,prices=prices, total=total)


### Build Guitar ###
@app.route("/build_your_own", methods=["GET", "POST"])
def build_your_own():
    form = BuildForm()
    message = ""
    if form.validate_on_submit():
        shape = form.shape.data
        colour = form.colour.data
        wood = form.wood.data
        pickup = form.pickup.data
        db = get_db()
        shape_row = db.execute("""SELECT price FROM shapes
                                WHERE shape = ?;""", (shape,)).fetchone()
        colour_row = db.execute("""SELECT price FROM colours
                                WHERE colour = ?;""", (colour,)).fetchone()
        wood_row = db.execute("""SELECT price FROM woods
                                WHERE wood_type = ?;""", (wood,)).fetchone()
        pickup_row = db.execute("""SELECT price FROM electronics
                                WHERE pickup_type = ?;""", (pickup,)).fetchone()
        db.commit()
        price = shape_row["price"] + colour_row["price"] + wood_row["price"] + pickup_row["price"]
        message = "Estimated total: " + str(price)
        
    return render_template("build_your_own.html", form=form, message=message)


### Get Quote ###
@app.route("/quote", methods=["GET", "POST"])
def quote():
    form=QuoteForm()
    if form.validate_on_submit():
        email = form.email.data
        response = make_response(render_template("index.html", message = "Thank you. Our team will be in contact with you shortly."))
        return response
    return render_template("quote.html", form=form)


### Logout ###
@app.route("/logout")
def logout():
    session.clear()
    return redirect( url_for("index") )


### Checkout ###
@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    if "cart" not in session:  
        session["cart"] = {}
    form = CheckoutForm()
    names = {}
    prices = {}
    total = 0
    price = 0
    db = get_db()
    for guitar_id in session["cart"]:
        guitar = db.execute("""SELECT * FROM guitars
                                WHERE guitar_id = ?;""", (guitar_id,)).fetchone()
        name = guitar["name"]
        names[guitar_id] = name
        price = guitar["price"]
        prices[guitar_id] = price
        quantity = session["cart"][guitar_id] * guitar["price"]
        total += quantity
    if form.validate_on_submit():
        first_name = form.first_name.data
        surname = form.surname.data
        address = form.address.data
        delivery_method = form.delivery_method.data
        for guitar_id in session['cart']:
            db = get_db()
            db.execute("""INSERT INTO orders ('guitar', 'first_name', 'surname', 'address', 'delivery_method','total')
                        VALUES (?,?,?,?,?,?);""", (names[guitar_id], first_name, surname,address, delivery_method, total))
            db.commit()
            if delivery_method == "Standard":
                response = make_response(render_template('index.html', message="Thank you for your order. Your guitar will be delivered in 3 to 5 days!")) 
            elif delivery_method == "Next Day":
                response = make_response(render_template('index.html', message="Thank you for your order. Your guitar will be delivered tomorrow!"))
            session.pop('cart',None)
            return response        
    return render_template("checkout.html",cart=session["cart"], form=form, names=names, prices=prices, total=total, price=price)
        

### Remove Cart ###
@app.route('/remove_cart')
def remove_cart():
    session.pop('cart',None)
    return redirect( url_for("cart") )


### Admin Login ###
@app.route("/admin", methods=["GET", "POST"])
def admin():
    form = AdminForm()
    message = ""
    if form.validate_on_submit():
        admin_id = form.admin_id.data
        admin_password = form.password.data
        db = get_db()
        matching_user = db.execute("""SELECT * FROM admin
                                    WHERE admin_id = ?;""",(admin_id,)).fetchone()
        if matching_user is None:
            form.admin_id.errors.append("Unknown admin id!")
        if check_password_hash(matching_user["admin_password"], admin_password):
            session.clear()
            session["admin_id"] = admin_id
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("update_stock")
            return redirect(next_page)
        else:
            form.password.errors.append("Incorrect password!")
    return render_template("admin.html", form=form, message=message)


### Update Stock ###
@app.route("/update_stock", methods=["GET", "POST"])
@admin_required
def update_stock():
    form=StockForm()
    message=""
    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        image=form.image.data
        description = form.description.data
        db = get_db()
        db.execute("""INSERT INTO guitars (name, price, image,description)
                        VALUES (?, ?, ?, ?)""", (name, price,image, description))
        db.commit()
        message = "Stock Updated"
    return render_template("update_stock.html", form=form, message=message)
    

### View Orders ###
@app.route("/orders")
def orders():
    db=get_db()
    orders = db.execute("""SELECT * FROM orders;""").fetchall()
    return render_template("orders.html",orders=orders, caption="Your orders")


       

# http://127.0.0.1:5000/admin
