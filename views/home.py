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
from flask_login import current_user, login_required
from app import owner, nft_address, w3, nft_instance
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
            owner=nft_instance.functions.ownerOf(int(collectible[:-4])).call(),
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

    # user wants to mint a collectible

    try:
        wei = w3.toWei(10, "ether")
        tx = {
            "from": current_user.id,
            "to": nft_address,
            "value": wei,
            "gas": 2000000,
            "gasPrice": w3.toWei("40", "gwei"),
        }
        tx_hash = nft_instance.functions.mint(int(id), collectible).transact(
            tx
        )
        bid_txn_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print(bid_txn_receipt)
        
    except Exception as e:
        flash(f"Error: {e['message']}", "danger")
    flash("Collectible minted successfully", "success")
    return redirect(url_for(".index"))

@home.route("/nft-operations", methods=["GET", "POST"])
def exec():
    if request.method == "GET":
        return render_template("nft_operations.html")
    operation = request.form.get("operation")
    if not operation:
        abort(400)
    if operation == "transferFrom":
        _from = request.form.get("from")
        to = request.form.get("to")
        token_id = request.form.get("tokenId")
        if not _from or not to or not token_id:
            abort(400)

        # validate the address
        if not w3.isAddress(_from) or not w3.isAddress(to):
            flash("Invalid address", "danger")
            return redirect(url_for(".exec"))

        try:
        # create the transaction
            wei = w3.toWei(10, "ether")
            tx = {
                "from": _from,
                "to": nft_address,
                "value": wei,
                "gas": 2000000,
                "gasPrice": w3.toWei("40", "gwei"),
            }
            tx_hash = nft_instance.functions.transferFrom1(
                _from, to, int(token_id)
            ).transact(tx)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print(tx_receipt)
            owner = nft_instance.functions.ownerOf(int(token_id)).call()
            print(owner)
        except Exception as e:
            print(e.args[0])
           
            return redirect(url_for(".exec"))
        print(nft_instance.functions.ownerOf(int(token_id)).call())
        flash("Collectible transferred successfully", "success")
        return redirect(url_for(".index"))
