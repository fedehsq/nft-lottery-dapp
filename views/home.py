import os
import random
from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, url_for
from app import local_acct, contract_address, w3, contract_instance


home = Blueprint("home", __name__)
# get all colletibles from static folder
collectibles = [
    collectible for collectible in os.listdir("./static/images/collectibles")
]


@home.route("/", methods=["GET", "POST"])
def index():
    # get ten random collectibles from the static folder
    random_collectibles = [
        collectible for collectible in random.choices(collectibles, k=10)
    ]
    return render_template("index.html", collectibles=random_collectibles)


@home.route("/mint", methods=["POST"])
def mint():
    collectible = request.form.get('collectible')
    # user wants to apply a promo
    if not collectible:
        # fake post requests
        abort(444)
    id = int(collectible[:-4])
    
    bid_amt_wei = w3.toWei(10, "ether")
    bid_txn_dict = {
        'from': local_acct.address,
        'to': contract_address,
        'value': bid_amt_wei,
        'gas': 2000000,
        'gasPrice': w3.toWei('40', 'gwei')
        }
    bid_txn_hash = contract_instance.functions.mint(id, collectible).transact(bid_txn_dict)
    bid_txn_receipt = w3.eth.waitForTransactionReceipt(bid_txn_hash)
    print(bid_txn_receipt)

    owner = contract_instance.functions.ownerOf(id).call()
    print(owner)
    
    flash(owner)
    return redirect(url_for(".index"))


