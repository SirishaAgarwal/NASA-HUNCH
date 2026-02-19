from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from models import db, User, Inventory
from datetime import datetime, date
import os

# ---------------- FLASK APP ---------------- #
app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret-key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- DB INIT ---------------- #
with app.app_context():
    db.create_all()

    if not User.query.filter_by(username="admin").first():
        pw_hash = bcrypt.generate_password_hash("admin123").decode("utf-8")
        admin = User(
            username="admin",
            password=pw_hash,
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()

# ---------------- LOGIN ---------------- #
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please fill in all fields")
            return redirect(url_for("login"))

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))

        flash("Invalid username or password")

    return render_template("login.html")


# ---------------- SIGNUP ---------------- #
@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        flash("Please fill in all fields")
        return redirect(url_for("login"))

    if User.query.filter_by(username=username).first():
        flash("Account already exists")
        return redirect(url_for("login"))

    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        username=username,
        password=pw_hash,
        role="crew"
    )

    db.session.add(user)
    db.session.commit()

    flash("Account created! Please login.")
    return redirect(url_for("login"))



# ---------------- DASHBOARD ---------------- #
@app.route("/dashboard")
@login_required
def dashboard():
    items = Inventory.query.all()

    total_kits = sum(item.quantity for item in items)
    low_stock = sum(1 for item in items if item.quantity <= 5)
    expired = sum(1 for item in items if item.expiration_date and item.expiration_date < date.today())
    checked_out = sum(item.checked_out for item in items)

    today = date.today()
    weekly_usage = [0] * 7

    for item in items:
        if item.last_checked_out:
            delta_days = (today - item.last_checked_out.date()).days
            if 0 <= delta_days <= 6:
                weekly_usage[item.last_checked_out.weekday()] += 1

    total_weekly_usage = sum(weekly_usage)
    avg_daily_usage = total_weekly_usage / 7 if total_weekly_usage else 0.5

    days_until_depletion = int(total_kits / avg_daily_usage) if avg_daily_usage else 180

    if days_until_depletion > 60:
        risk = "NOMINAL"
    elif days_until_depletion > 30:
        risk = "CAUTION"
    else:
        risk = "CRITICAL"

    return render_template(
        "dashboard.html",
        total_kits=total_kits,
        low_stock=low_stock,
        expired=expired,
        checked_out=checked_out,
        inventory=items,
        current_date=today,
        weekly_usage=weekly_usage,
        days_until_depletion=days_until_depletion,
        risk=risk
    )

# ---------------- LOGOUT ---------------- #
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ---------------- INVENTORY ---------------- #
@app.route("/inventory", methods=["GET", "POST"])
@login_required
def inventory():
    if current_user.role != "admin":
        return "Access denied"

    if request.method == "POST":
        exp_date = None
        exp_str = request.form.get("expiration_date")

        if exp_str:
            exp_date = datetime.strptime(exp_str, "%Y-%m-%d").date()

        item = Inventory(
            item_name=request.form["item_name"],
            quantity=int(request.form["quantity"]),
            expiration_date=exp_date
        )

        db.session.add(item)
        db.session.commit()

    return render_template("inventory.html", inventory=Inventory.query.all())

#----------------EDIT--------------#
@app.route("/inventory/edit/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit_item(item_id):
    if current_user.role != "admin":
        flash("Admin access required.")
        return redirect(url_for("dashboard"))

    item = Inventory.query.get_or_404(item_id)

    if request.method == "POST":
        item.item_name = request.form["item_name"]
        item.quantity = int(request.form["quantity"])

        exp_str = request.form.get("expiration_date")
        if exp_str:
            item.expiration_date = datetime.strptime(exp_str, "%Y-%m-%d").date()
        else:
            item.expiration_date = None

        db.session.commit()
        flash("Item updated successfully.")
        return redirect(url_for("inventory"))

    return render_template("edit_item.html", item=item)

# ---------------- RUN ---------------- #
if __name__ == "__main__":
    app.run(debug=True)
