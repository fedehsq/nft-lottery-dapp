from audioop import add
import os
import random
from flask import (
    Blueprint,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from app import local_acct, contract_address, w3, contract_instance
from processors.nft_collectible import NftCollectible


auth = Blueprint("auth", __name__)
# get all colletibles from static folder
images = [
    image for image in os.listdir("./static/images/collectibles")
]


@auth.route("/", methods=["GET", "POST"])
def index():
    # get ten random collectibles from the static folder
    collectibles = [
        NftCollectible(
            id=int(collectible[:-4]),
            collectible=collectible,
            owner=contract_instance.functions.ownerOf(int(collectible[:-4])).call(),
        )
        for collectible in images[0: 10]
    ]
    return render_template("index.html", collectibles=collectibles)


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
        return redirect(url_for("home.index"))
    else:
        flash("Invalid address", "danger")
        return render_template("login.html")
    
