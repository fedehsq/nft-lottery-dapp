from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_user
from app import w3
from auth import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
        
    address = request.form.get("address")
    if not address:
        abort(400)
    if w3.isAddress(address):
        session['address'] = address
        flash("Successfully authenticated", "success")
        login_user(User(address))
        return redirect(url_for("home.index"))
    else:
        flash("Invalid address", "danger")
        return render_template("login.html")
    
