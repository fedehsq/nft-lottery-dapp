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
from flask_login import current_user, login_required, login_user, logout_user
from app import COLLECTIBLES, w3, manager
from auth import User

auth = Blueprint("auth", __name__)

@auth.route("/auth/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", next_url = request.args.get("next"), accounts = w3.eth.accounts)
    address = request.form.get("address")
    next_url = request.form.get("next_url")
    print(next_url)
    if not address:
        abort(400)
    if w3.isAddress(address) and address in w3.eth.accounts:
        session['address'] = address
        flash("Successfully authenticated", "success")
        login_user(User(address, True if address == manager.address else False))
        return redirect(next_url or url_for("home.index"))
    else:
        flash("Invalid address")
        return render_template("login.html", accounts = w3.eth.accounts)


@auth.route("/auth/account", methods=["GET"])
@login_required
def account():
    wei_balance = w3.eth.getBalance(current_user.id)
    eth_balance = w3.fromWei(wei_balance, "ether")
    # Get all collectibles owned by the user
    collectibles = []
    for collectible in COLLECTIBLES.values():
        if collectible.owner == current_user.id:
            collectibles.append(collectible)

    return render_template(
        "account.html", balance=eth_balance, collectibles=collectibles
    )
    

@auth.route("/auth/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    session.clear()
    flash("Successfully logged out")
    return redirect(url_for("home.index"))
    
