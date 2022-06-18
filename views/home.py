import os
from flask import (
    render_template,
    Blueprint,
)
from flask import session
from app import w3, nft_instance
from flask import jsonify
from processors.nft_collectible import NftCollectible
from app import (
    lottery_closed_event,
    lottery_created_event,
    round_opened_event,
    ticket_bought_event,
    winning_numbers_drawn,
    token_minted_event,
)


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
    return render_template(
        "index.html",
        collectibles=collectibles,
        slideshow_collectibles=slideshow_collectibles,
    )


@home.route("/accounts", methods=["GET"])
def accounts():
    return render_template("accounts.html", accounts=w3.eth.accounts)


@home.route("/notifications", methods=["GET"])
def notifications():
    # get all events from the lottery contract
    events_entries = (
        lottery_created_event.get_new_entries()
        + lottery_closed_event.get_new_entries()
        + round_opened_event.get_new_entries()
        + ticket_bought_event.get_new_entries()
        + winning_numbers_drawn.get_new_entries()
        + token_minted_event.get_new_entries()
    )

    print(events_entries)
    print(events_entries)
    print(events_entries)

    if len(events_entries) > 0:
        events = [event.get("event") for event in events_entries]
        return jsonify(status=200, events=events)
    else:
        return jsonify(status=204)
