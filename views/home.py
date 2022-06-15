import os
from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required
from app import local_acct, contract_address, w3, contract_instance
from processors.nft_collectible import NftCollectible


home = Blueprint("home", __name__)
# get all colletibles from static folder
images = [
    image for image in os.listdir("./static/images/collectibles")
]


@home.route("/", methods=["GET", "POST"])
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

@home.route("/accounts", methods=["GET"])
def accounts():
    return render_template("accounts.html", accounts=w3.eth.accounts)


@home.route("/mint", methods=["POST"])
@login_required
def mint():
    collectible = request.form.get("collectible")
    id = request.form.get("collectibleId")
    # user wants to apply a promo
    if not collectible and not id: 
        # fake post requests
        abort(444)

    wei = w3.toWei(10, "ether")
    tx = {
        "from": local_acct.address,
        "to": contract_address,
        "value": wei,
        "gas": 2000000,
        "gasPrice": w3.toWei("40", "gwei"),
    }
    tx_hash = contract_instance.functions.mint(int(id), collectible).transact(
        tx
    )
    bid_txn_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print(bid_txn_receipt)
    flash("Collectible minted successfully", "success")
    return redirect(url_for(".index"))
