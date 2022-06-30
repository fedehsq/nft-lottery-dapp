import random
from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required
from app import COLLECTIBLES, TICKETS
from auth import deployed_required, manager_required, user_required
from helpers.ticket import Ticket
from processors.contract import ContractProcessor
from processors.lottery import LotteryProcessor
from processors.nft import NftProcessor
from app import w3


lottery = Blueprint("lottery", __name__)


@lottery.route("/lottery", methods=["GET"])
@login_required
def lottery_home():
    """
    Render the lottery homepage
    """
    if current_user.is_admin:
        return render_template("manager_lottery.html")
    else:
        is_open = False
        if ContractProcessor.LOTTERY_DEPLOYED:
            is_open = LotteryProcessor.is_open()
        return render_template(
            "user_lottery.html",
            is_open=is_open,
            registered=session.get("starting_block", None),
        )


@lottery.route("/lottery/register-user", methods=["GET"])
@login_required
@user_required
def register_user():
    """
    Register the user for the lottery
    """
    if not session.get("starting_block"):
        LotteryProcessor.init_filters.submit()
        session["starting_block"] = w3.eth.block_number if w3.eth.block_number else 1
        flash("You have been registered for the lottery")
        print(session.get("starting_block"))
        return redirect(url_for("lottery.lottery_home"))
    else:
        flash("You have already registered for the lottery")
        return redirect(url_for("lottery.lottery_home"))


@lottery.route("/lottery/mint", methods=["POST"])
@login_required
@manager_required
@deployed_required
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
    rank = random.randint(1, 8)
    tx_result = LotteryProcessor.mint(collectible.id, collectible.collectible, rank)
    if tx_result:
        flash("Collectible minted successfully")
        COLLECTIBLES[int(id)].owner = NftProcessor.owner_of(collectible.id)
        COLLECTIBLES[int(id)].rank = rank
        return redirect(request.referrer or url_for("home.index"))

    # Check if the lottery is open
    if not LotteryProcessor.is_open():
        flash("The lottery is closed")
        return redirect(request.referrer or url_for("lottery.lottery_home"))

    # Check if the token is already owned
    if LotteryProcessor.is_already_minted(int(id)):
        flash("The token is already owned")
        return redirect(request.referrer or url_for("lottery.lottery_home"))

    flash("Error during minting")
    return redirect(request.referrer or url_for("home.index"))


@lottery.route("/lottery/tickets", methods=["GET"])
@login_required
@deployed_required
def tickets():
    """
    Display the tickets.
    If the user the manager, display all the tickets.
    If the user is the user, display only the tickets that he owns.
    """
    if current_user.is_admin:
        return render_template("tickets.html", tickets=TICKETS)
    else:
        return render_template(
            "tickets.html",
            tickets=[ticket for ticket in TICKETS if ticket.buyer == current_user.id],
        )


@lottery.route("/lottery/buy-ticket", methods=["POST"])
@login_required
@user_required
@deployed_required
def buy_ticket():
    """
    Buy a ticket for the current user and redirect to the home page if the transaction is successful.
    Else, flash a message and redirect to the home page.
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
        return redirect(url_for(".lottery_home"))

    # Check if the lottery is open
    if not LotteryProcessor.is_open():
        flash("The lottery is closed")
        return redirect(url_for("lottery.lottery_home"))

    # Check if the round is active
    if not LotteryProcessor.is_round_active():
        flash("The round is not active")
        return redirect(url_for("lottery.lottery_home"))

    # Generic error message
    flash("Error during buying tickets")
    return redirect(url_for("lottery.lottery_home"))


@lottery.route("/lottery/create-lottery", methods=["GET"])
@login_required
@manager_required
def create_lottery():
    """
    Create the lottery and redirect to the lottery page if the transaction is successful,
    otherwise redirect to the lottery home page.
    """
    # Deploy the smart contracts
    if not ContractProcessor.LOTTERY_DEPLOYED:
        if ContractProcessor.deploy_contracts():
            flash("Lottery deployed successfully")
            return redirect(url_for("lottery.lottery_home"))
        else:
            flash("Error during lottery deployment")
            return redirect(url_for("lottery.lottery_home"))

    # Check if the lottery is open
    if LotteryProcessor.is_open():
        flash("The lottery is already open")
        return redirect(url_for("lottery.lottery_home"))

    else:
        flash("The lottery is closed")
        return redirect(request.referrer or url_for("lottery.lottery_home"))


@lottery.route("/lottery/open-round", methods=["GET"])
@login_required
@manager_required
@deployed_required
def open_round():
    """
    Open the lottery round and redirect to the lottery page in case of success
    else, flash a message and redirect to the lottery page.
    """
    tx_result = LotteryProcessor.open_round()
    if tx_result:
        flash("Round opened successfully")
        return redirect(url_for("lottery.lottery_home"))

    # Check if the lottery is open
    if not LotteryProcessor.is_open():
        flash("The lottery is closed")
        return redirect(url_for("lottery.lottery_home"))

    # Check if the round is active
    if LotteryProcessor.is_round_active():
        flash("The round is already active")
        return redirect(url_for("lottery.lottery_home"))

    # Check if the round is finished
    if not LotteryProcessor.is_round_finished():
        flash("The round is not finished")
        return redirect(url_for("lottery.lottery_home"))

    # Check if the winning ticket is already set
    if not LotteryProcessor.is_winning_ticket_extracted():
        flash("The winning ticket is not extracted")
        return redirect(url_for("lottery.lottery_home"))

    flash("Error during opening")
    return redirect(url_for(".lottery_home"))


@lottery.route("/lottery/close-lottery", methods=["GET"])
@login_required
@manager_required
@deployed_required
def close_lottery():
    """
    Close the lottery and redirect to the lottery page in case of success
    else the error message is displayed.
    """

    tx_result = LotteryProcessor.close_lottery()
    if tx_result:
        flash("Lottery closed successfully")
        TICKETS.clear()
        return redirect(url_for("lottery.lottery_home"))

    # Check if the lottery is open
    if not LotteryProcessor.is_open():
        flash("The lottery is already closed")
        return redirect(url_for("lottery.lottery_home"))

    flash("Error during closing")
    return redirect(url_for(".lottery_home"))


@lottery.route("/lottery/extract-winning-ticket", methods=["GET"])
@login_required
@manager_required
@deployed_required
def extract_winning_ticket():
    tx_result = LotteryProcessor.extract_winning_ticket()
    if tx_result:
        flash("Winning ticket extracted successfully")
        return redirect(url_for(".lottery_home"))

    # Check if the lottery is open
    if not LotteryProcessor.is_open():
        flash("The lottery is closed")
        return redirect(url_for("lottery.lottery_home"))

    # Check if the round is active
    if LotteryProcessor.is_round_active():
        flash("The round is already active")
        return redirect(url_for("lottery.lottery_home"))

    # Check if the round is finished
    if LotteryProcessor.is_round_finished():
        flash("The round is finished")
        return redirect(url_for("lottery.lottery_home"))

    # Check if the winning ticket is already extracted
    if LotteryProcessor.is_winning_ticket_extracted():
        flash("The winning ticket is already extracted")
        return redirect(url_for("lottery.lottery_home"))

    flash("Error during extraction")
    return redirect(url_for(".lottery_home"))


@lottery.route("/lottery/give-prizes", methods=["GET"])
@login_required
@manager_required
@deployed_required
def give_prizes():
    """
    Give the prizes to the winners and redirect to the lottery page in case of success
    else the error message is displayed.
    """

    tx_result = LotteryProcessor.give_prizes()
    if tx_result:
        flash("Prizes given successfully")
        # Clear the tickets
        TICKETS.clear()
        return redirect(url_for(".lottery_home"))

    # Check if the lottery is open
    if not LotteryProcessor.is_open():
        flash("The lottery is closed")
        return redirect(url_for("lottery.lottery_home"))

    # Check if the round is active
    if LotteryProcessor.is_round_active():
        flash("The round is not yet finished")
        return redirect(url_for("lottery.lottery_home"))

    # Check if the round is finished
    if LotteryProcessor.is_round_finished():
        flash("The round is finished")
        return redirect(url_for("lottery.lottery_home"))

    # Check if the winning ticket is already extracted
    if not LotteryProcessor.is_winning_ticket_extracted():
        flash("The winning ticket is not yet extracted")
        return redirect(url_for("lottery.lottery_home"))

    flash("Error during giving prizes")
    return redirect(url_for(".lottery_home"))
