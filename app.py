import json
import os
import random
from web3 import Web3, HTTPProvider
from flask import Flask
from processors.contract import ContractProcessor
from config import Development
from helpers.nft_collectible import NftCollectible
from processors.lottery import LotteryProcessor

ROUND_DURATION = 2
# create a web3.py instance w3 by connecting to the local Ethereum node
w3 = Web3(HTTPProvider("http://localhost:8545"))

# Initialize a local account object from the private key of a valid Ethereum node address
# Get the private key from the json file 'keys.json'
manager_pkey = open("./keys.json").read()
manager_pkey = json.loads(manager_pkey)["private_keys"][w3.eth.accounts[0].lower()]
manager = w3.eth.account.from_key(
    manager_pkey
)

# Nft contract address and ABI
nft_address, nft_instance = ContractProcessor.deploy_contract("NFT")

# Lottery contract address and ABI (pass Nft contract address as parameter)
lottery_address, lottery_instance = ContractProcessor.deploy_contract(
    "Lottery", nft_address, ROUND_DURATION
)

# Initialize the lottery filters for the events
LotteryProcessor.init_filters()

# Create all the collectibles as map of key:value pairs
COLLECTIBLES = dict(
    [
        (
            int(collectible[:-4]),
            NftCollectible(
                id=int(collectible[:-4]),
                collectible=collectible,
                rank=0,
                owner=ContractProcessor.ADDRESS_ZERO,
            ),
        )
        for collectible in os.listdir("./static/images/collectibles")
    ]
)

TICKETS = []

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

    return app


if __name__ == "__main__":
    app = create_app(config=Development)
    app.run(debug=True)
