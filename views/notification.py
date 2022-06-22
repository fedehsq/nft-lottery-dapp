from flask import (
    Blueprint,
    session,
)
from flask import jsonify
from app import (
    lottery_closed_event,
    lottery_created_event,
    round_opened_event,
    ticket_bought_event,
    winning_numbers_drawn,
    token_minted_event,
    prize_assigned,
    round_finished
)
from processors.nft import NftProcessor
from app import COLLECTIBLES

notification = Blueprint("notification", __name__)


@notification.route("/notifications", methods=["GET"])
def notifications():
    """
    Get all events from the lottery contract.
    return: status 200 and json object of all notifications if any else 204 (no content) status
    """
    events_entries = (
        lottery_created_event.get_all_entries()
        + lottery_closed_event.get_all_entries()
        + round_opened_event.get_all_entries()
        + ticket_bought_event.get_all_entries()
        + winning_numbers_drawn.get_all_entries()
        + token_minted_event.get_all_entries()
        + prize_assigned.get_all_entries()
        + round_finished.get_all_entries()
    )

    for e in events_entries:
        print(e)
        print("\n")

    events = []
    for e in events_entries:
        block_id = str(e.blockNumber)
        event = e.event
        args = e.args
        # Check if the event is already notified
        if not session.get(block_id):
            session[block_id] = []
        if event not in session.get(block_id):
            # check if the event is 'TokenMinted' or 'PrizeAssigned' to update the owner of the collectible
            if event == "TokenMinted" or event == "PrizeAssigned":
                # Update the owner of the collectible
                token_id = int(args._tokenId)
                COLLECTIBLES[token_id].owner = NftProcessor.owner_of(token_id)
            session[block_id].append(event)
            events.append(event + ": " + str(args))

    session["events"] = session.get("events", []) + events

    if len(events) > 0:
        return jsonify(
            status=200, events=events, non_read_events=session.get("events", [])
        )
    else:
        return jsonify(status=204)


@notification.route("/notifications/delete-all", methods=["GET"])
def delete_notifications():
    """
    Delete all notifications.
    :return: status code
    """
    session.pop("events", None)
    return jsonify(status=200)
