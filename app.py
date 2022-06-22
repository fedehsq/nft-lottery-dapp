import os
import random
from web3 import Web3, HTTPProvider
from flask import Flask
from processors.contract import ContractProcessor
from config import Development
from helpers.nft_collectible import NftCollectible


# create a web3.py instance w3 by connecting to the local Ethereum node
w3 = Web3(HTTPProvider("http://localhost:8545"))

# Initialize a local account object from the private key of a valid Ethereum node address
manager = w3.eth.account.from_key(
    "0x66dcd9687ae40be21d392b95a25cef6017a11f3ffed9e885b7cda9c01a22e470"
)

# Nft contract address and ABI
nft_address, nft_instance = ContractProcessor.deploy_contract("NFT")

# Lottery contract address and ABI (pass Nft contract address as parameter)
lottery_address, lottery_instance = ContractProcessor.deploy_contract(
    "Lottery", nft_address, 2
)


# Filter for Lottery events
lottery_created_event = lottery_instance.events.LotteryCreated.createFilter(
    fromBlock=1, toBlock="latest"
)

# Filter for Lottery events
round_opened_event = lottery_instance.events.RoundOpened.createFilter(
    fromBlock=1, toBlock="latest"
)

# Filter for Lottery events
lottery_closed_event = lottery_instance.events.LotteryClosed.createFilter(
    fromBlock=1, toBlock="latest"
)

# Filter for Lottery events
token_minted_event = lottery_instance.events.TokenMinted.createFilter(
    fromBlock=1, toBlock="latest"
)

# Filter for Lottery events
ticket_bought_event = lottery_instance.events.TicketBought.createFilter(
    fromBlock=1, toBlock="latest"
)

# Filter for Lottery events
winning_numbers_drawn = lottery_instance.events.WinningNumbersDrawn.createFilter(
    fromBlock=1, toBlock="latest"
)

# Filter for Lottery events
prize_assigned = lottery_instance.events.PrizeAssigned.createFilter(
    fromBlock=1, toBlock="latest"
)

# Filter for Lottery events
round_finished = lottery_instance.events.RoundFinished.createFilter(
    fromBlock=1, toBlock="latest"
)

# Create all the collectibles as map of key:value pairs
COLLECTIBLES = dict(
    [
        (
            int(collectible[:-4]),
            NftCollectible(
                id=int(collectible[:-4]),
                collectible=collectible,
                rank=random.randint(1, 8),
                owner=ContractProcessor.ADDRESS_ZERO,
            ),
        )
        for collectible in os.listdir("./static/images/collectibles")
    ]
)

def create_app(config="config.Development"):
    """
    Create the flask app register the blueprints
    """
    from views.home import home
    from views.auth import auth
    from views.lottery import lottery
    from views.notification import notification
    import auth as lm

    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(lottery)
    app.register_blueprint(notification)
    lm.init_login_manager(app)

    """@app.before_first_request
    def before_first_request():
        listen_for_events.submit()"""

    return app


if __name__ == "__main__":
    app = create_app(config=Development)
    app.run(debug=True)
