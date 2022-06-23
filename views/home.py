from flask import (
    render_template,
    Blueprint,
    request,
)
from app import w3, COLLECTIBLES

home = Blueprint("home", __name__)


@home.route("/", methods=["GET", "POST"])
def index():
    return render_template(
        "index.html",
        collectibles=[COLLECTIBLES.get(key) for key in range(1, 10)],
        slideshow_collectibles=[COLLECTIBLES.get(key) for key in range(10, 20)],
        accounts=w3.eth.accounts
    )


@home.route("/accounts", methods=["GET"])
def accounts():
    return render_template("accounts.html", accounts=w3.eth.accounts)


@home.route("/collectibles", methods=["GET"])
def collectibles():
    # display 100 collectibles per page
    arg = request.args.get("search", None)
    if arg:
        collectibles = [
            collectible
            for collectible in COLLECTIBLES.values()
            if collectible.collectible == arg or collectible.owner == arg
        ]
        return render_template(
            "collectibles.html",
            collectibles=collectibles,
            n_pages=1,
            n_page=1,
            accounts=w3.eth.accounts
        )

    n_page = int(request.args.get("page", 1))
    n_collectibles = len(COLLECTIBLES)
    n_pages = n_collectibles // 100 + 1
    if n_page > n_pages:
        n_page = n_pages
    collectibles = [
        COLLECTIBLES.get(key) for key in range(n_page * 100 - 99, n_page * 100)
    ]
    return render_template(
        "collectibles.html",
        collectibles=collectibles,
        n_pages=n_pages,
        n_page=n_page,
        accounts=w3.eth.accounts
    )
