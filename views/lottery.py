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
from app import COLLECTIBLES, lottery_instance
from auth import manager_required
from processors.lottery import LotteryProcessor
from processors.nft import NftProcessor


lottery = Blueprint("lottery", __name__)


@lottery.route("/lottery", methods=["GET"])
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
def open_round():
    tx_result = LotteryProcessor.close_lottery()
    if tx_result:
        flash("Lottery closed successfully")
    else:
        flash("Error during closing")
    return redirect(url_for(".lottery_home"))

@lottery.route("/lottery/extract-winning-ticket", methods=["GET"])
@login_required
@manager_required
def open_round():
    tx_result = LotteryProcessor.close_lottery()
    if tx_result:
        flash("Lottery closed successfully")
    else:
        flash("Error during closing")
    return redirect(url_for(".lottery_home"))

