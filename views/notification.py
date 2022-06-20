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
)

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
    )

    events = []
    for event in events_entries:
        block_id = str(event.blockNumber)
        # Check if the event is already notified
        if not session.get(block_id):
            session[block_id] = block_id
            events.append(event.get('event'))
            
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
