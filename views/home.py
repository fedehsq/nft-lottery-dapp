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
    slideshow_collectibles = [
        NftCollectible(
            id=int(collectible[:-4]),
            collectible=collectible,
            owner=nft_instance.functions.ownerOf(int(collectible[:-4])).call(),
        )
        for collectible in images[10:20]
    ]
    return render_template("index.html", collectibles=collectibles,slideshow_collectibles=slideshow_collectibles)


@home.route("/accounts", methods=["GET"])
def accounts():
    return render_template("accounts.html", accounts=w3.eth.accounts)

@home.route("/notifications", methods=["GET"])
def notifications():
    from app import event_filter
    events_entries = event_filter.get_new_entries()
    if len(events_entries) > 0:
        events = [event.get("event") for event in events_entries]
        return jsonify(status=200, events=events)
    else:
        return jsonify(status=204)