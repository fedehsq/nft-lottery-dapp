import os
from flask import (
    render_template,
    Blueprint,
)
from flask import session
from app import w3, nft_instance
from flask import jsonify
from processors.nft_collectible import NftCollectible


home = Blueprint("home", __name__)
# get all colletibles from static folder
images = [image for image in os.listdir("./static/images/collectibles")]


@home.route("/", methods=["GET", "POST"])
def index():
    # get ten random from the static folder and display them into the slider
    collectibles = [
        NftCollectible(
            id=int(collectible[:-4]),
            collectible=collectible,
            owner=nft_instance.functions.ownerOf(int(collectible[:-4])).call(),
        )
        for collectible in images[0:10]
    ]
    return render_template("index.html", collectibles=collectibles)


@home.route("/accounts", methods=["GET"])
def accounts():
    return render_template("accounts.html", accounts=w3.eth.accounts)

@home.route("/notification", methods=["GET"])
def notification():
    from app import event_filter
    events = event_filter.get_new_entries()
    if len(events) > 0:
        return jsonify(status=200, events=events)
    else:
        return jsonify(status=204)