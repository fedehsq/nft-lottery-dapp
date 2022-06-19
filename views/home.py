import os
from flask import (
    render_template,
    Blueprint,
)
from app import w3, COLLECTIBLES
from flask import jsonify
from app import (
    lottery_closed_event,
    lottery_created_event,
    round_opened_event,
    ticket_bought_event,
    winning_numbers_drawn,
    token_minted_event,
)


home = Blueprint("home", __name__)

@home.route("/", methods=["GET", "POST"])
def index():
    from app import nft_address, lottery_address
    print(nft_address)
    print(lottery_address)
    return render_template(
        "index.html",
        collectibles=[COLLECTIBLES.get(key) for key in range(1, 10)],
        slideshow_collectibles=[COLLECTIBLES.get(key) for key in range(10, 20)],
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
