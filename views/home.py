from flask import (
    render_template,
    Blueprint,
)
from app import w3, COLLECTIBLES

home = Blueprint("home", __name__)


@home.route("/", methods=["GET", "POST"])
def index():
    return render_template(
        "index.html",
        collectibles=[COLLECTIBLES.get(key) for key in range(1, 10)],
        slideshow_collectibles=[COLLECTIBLES.get(key) for key in range(10, 20)],
    )


@home.route("/accounts", methods=["GET"])
def accounts():
    return render_template("accounts.html", accounts=w3.eth.accounts)
