from flask import (
    Blueprint,
    session,
)
from flask import jsonify
from processors.lottery import LotteryProcessor
from processors.nft import NftProcessor
from app import COLLECTIBLES

notification = Blueprint("notification", __name__)


@notification.route("/notifications", methods=["GET"])
def notifications():
    """
    Get all events from the lottery contract.
    return: status 200 and json object of all notifications if any
    else 204 (no content / user not interested in the lottery)
    """
    if not "starting_block" in session:
        return jsonify(status=204)

    events_entries = (
        LotteryProcessor.lottery_created_event.get_all_entries()
        + LotteryProcessor.lottery_closed_event.get_all_entries()
        + LotteryProcessor.round_opened_event.get_all_entries()
        + LotteryProcessor.winning_numbers_drawn_event.get_all_entries()
        + LotteryProcessor.prize_assigned.get_all_entries()
        + LotteryProcessor.token_minted.get_all_entries()
    )

    # order the events by block number in ascending order
    events_entries.sort(key=lambda x: x.blockNumber)

    events = []
    for e in events_entries:
        print(e, "\n")
        block_id = e.blockNumber
        event = e.event
        args = e.args
        log_index = e.logIndex
        # Avoid notifications if they was generated before the user logged in
        if block_id <= session.get("starting_block"):
            continue
        block_id = str(e.blockNumber)
        # Check if the event is already notified
        if not session.get(block_id):
            session[block_id] = []
        if (event, log_index) not in session.get(block_id):
            # check if the event is 'TokenMinted' or 'PrizeAssigned' to update the owner of the collectible
            if event == "TokenMinted" or event == "PrizeAssigned":
                # Update the owner of the collectible
                token_id = int(args._tokenId)
                COLLECTIBLES[token_id].owner = NftProcessor.owner_of(token_id)
                # Assign the proper rank to the collectible
                if event ==  "PrizeAssigned":
                    COLLECTIBLES[token_id].rank = int(args._rank)
            # Not display the event if the event is 'TokenMinted'
            if event == "TokenMinted":
                continue
            session[block_id].append((event, log_index))
            # get all arguments of the event
            str_args = ""
            for k, v in args.items():
                str_args += f"{k}: {v}; "
            events.append(event + "(" + str_args + ")")

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
