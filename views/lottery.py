from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required
from app import w3
from auth import owner_required
from processors.contract import ContractProcessor


lottery = Blueprint("lottery", __name__)


@lottery.route("/lottery", methods=["GET"])
def lottery_home():
    return render_template("lottery.html")


@lottery.route("/lottery/mint", methods=["POST"])
@login_required
@owner_required
def mint():
    collectible = request.form.get("collectible")
    id = request.form.get("collectibleId")
    if not collectible and not id:
        abort(400)
    # Mint a collectible
    tx_result = ContractProcessor.mint(int(id), collectible)
    if tx_result:
        flash("Collectible minted successfully", "success")
    else:
        flash("Error during minting")
    return redirect(url_for("home.index"))


"""@lottery.route("/lottery/transfer-from", methods=["POST"])
@login_required
def transfer_from():
    _from = request.form.get("from")
    to = request.form.get("to")
    token_id = request.form.get("tokenId")
    if not _from or not to or not token_id:
        abort(400)

    if not w3.isAddress(_from) or not w3.isAddress(to):
        flash("Invalid address", "danger")
        return redirect(url_for(".lottery"))

    # Transfer a collectible
    tx_result = ContractProcessor.transfer_from(_from, to, int(token_id))
    if tx_result:
        flash("Token transfered successfully", "success")
    else:
        flash("Error during transfer from")
    return redirect(url_for(".lottery"))"""
