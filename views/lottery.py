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
from app import COLLECTIBLES, TICKETS, lottery_instance
from auth import manager_required, user_required
from helpers.ticket import Ticket
from processors.lottery import LotteryProcessor
from processors.nft import NftProcessor


lottery = Blueprint("lottery", __name__)


@lottery.route("/lottery", methods=["GET"])
@login_required
def lottery_home():
    return render_template("lottery.html")


@lottery.route("/lottery/mint", methods=["POST"])
@login_required
@manager_required
def mint():
    """
    Mint a new token for the current user, and redirect to the home page.
    If the user is not the owner, flash a message and redirect to the home page.
    If the user is the owner, mint a new token and redirect to the home page.
    """
    collectible = request.form.get("collectible")
    id = request.form.get("collectibleId")
    if not collectible and not id:
        abort(400)
    collectible = COLLECTIBLES.get(int(id))
    tx_result = LotteryProcessor.mint(
        collectible.id, collectible.collectible, collectible.rank
    )
    if tx_result:
        flash("Collectible minted successfully")
        COLLECTIBLES[int(id)].owner = NftProcessor.owner_of(collectible.id)
    else:
        flash("Error during minting")
    return redirect(url_for("home.index"))

@lottery.route("/lottery/tickets", methods=["GET"])
@login_required
def tickets():
    """
    Display the tickets.
    If the user the manager, display all the tickets.
    If the user is the user, display only the tickets that he owns.
    """
    if current_user.is_admin:
        return render_template("tickets.html", tickets=TICKETS)
    else:
        return render_template("tickets.html", tickets=[ticket for ticket in TICKETS if ticket.buyer == current_user.id])

@lottery.route("/lottery/buy-ticket", methods=["POST"])
@login_required
@user_required
def buy_ticket():
    """
    Buy a ticket for the current user.
    """
    one = int(request.form.get("one"))
    two = int(request.form.get("two"))
    three = int(request.form.get("three"))
    four = int(request.form.get("four"))
    five = int(request.form.get("five"))
    powerball = int(request.form.get("powerball"))
    if not one or not two or not three or not four or not five or not powerball:
        abort(400)
    tx_result = LotteryProcessor.buy_ticket(one, two, three, four, five, powerball)
    if tx_result:
        flash("Tickets bought successfully")
        TICKETS.append(
            Ticket(
                buyer=current_user.id,
                one=one,
                two=two,
                three=three,
                four=four,
                five=five,
                powerball=powerball,
            )
        )
    else:
        flash("Error during buying")
    return redirect(url_for(".lottery_home"))


@lottery.route("/lottery/create-lottery", methods=["GET"])
@login_required
@manager_required
def create_lottery():
    """
    Create the lottery and redirect to the lottery page.
    """
    tx_result = LotteryProcessor.create_lottery()
    if tx_result:
        flash("Lottery created successfully")
    else:
        flash("Error during creation")
    return redirect(url_for(".lottery_home"))


@lottery.route("/lottery/open-round", methods=["GET"])
@login_required
@manager_required
def open_round():
    tx_result = LotteryProcessor.open_round()
    if tx_result:
        flash("Round opened successfully")
    else:
        flash("Error during opening")
    return redirect(url_for(".lottery_home"))


@lottery.route("/lottery/close-lottery", methods=["GET"])
@login_required
@manager_required
def close_lottery():
    tx_result = LotteryProcessor.close_lottery()
    if tx_result:
        flash("Lottery closed successfully")
    else:
        flash("Error during closing")
    return redirect(url_for(".lottery_home"))


@lottery.route("/lottery/extract-winning-ticket", methods=["GET"])
@login_required
@manager_required
def extract_winning_ticket():
    tx_result = LotteryProcessor.extract_winning_ticket()
    if tx_result:
        flash("Winning ticket extracted successfully")
    else:
        flash("Error during extraction")
    return redirect(url_for(".lottery_home"))


@lottery.route("/lottery/give-prizes", methods=["GET"])
@login_required
@manager_required
def give_prizes():
    tx_result = LotteryProcessor.give_prizes()
    if tx_result:
        flash("Prizes given successfully")
    else:
        flash("Error during giving prizes")
    return redirect(url_for(".lottery_home"))
