import os
import random
from flask import Blueprint, abort, jsonify, render_template, request
from nft_contract import nft, local_account, contract_address, w3


home = Blueprint("home", __name__)
# get all colletibles from static folder
collectibles = [
    collectible for collectible in os.listdir("./static/images/collectibles")
]


@home.route("/", methods=["GET", "POST"])
def index():
    owner = nft.functions.ownerOf(1).call()
    # get ten random collectibles from the static folder
    random_collectibles = [
        collectible for collectible in random.choices(collectibles, k=10)
    ]
    return render_template("index.html", owner=owner, collectibles=random_collectibles)


@home.route("/mint", methods=["POST"])
def mint():
    collectible = request.form.get('collectible')
    # user wants to apply a promo
    if not collectible:
        # fake post requests
        abort(444)
    id = int(collectible[:-4])

    bid_txn_dict = {
            'from': local_account.address,
            'to': contract_address,
            'value': w3.toWei(10, "ether"),
            'gas': 2000000,
            'gasPrice': w3.toWei('40', 'gwei')
        }
    bid_txn_hash = nft.functions.mint(id, collectible).transact(bid_txn_dict)
    bid_txn_receipt = w3.eth.waitForTransactionReceipt(bid_txn_hash)
    print(bid_txn_receipt)

    owner = nft.functions.ownerOf(id).call()
    
    print(owner)
    return jsonify(status=200)


