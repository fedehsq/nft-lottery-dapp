from time import sleep
from flask_executor import Executor
from web3 import Web3, HTTPProvider
from flask import Flask
from processors.contract import ContractProcessor
from config import Development


# create a web3.py instance w3 by connecting to the local Ethereum node
w3 = Web3(HTTPProvider("http://localhost:8545"))
# Initialize a local account object from the private key of a valid Ethereum node address
owner = w3.eth.account.from_key(
    "0x96d63edb92a1815e6fcd51b3ec2bd91c634feea5248da7521a60a0f94f4cd3fe"
)

nft_address, nft_instance = ContractProcessor.deploy_contract("NFT")
event_filter = nft_instance.events.Transfer.createFilter(fromBlock=1, toBlock="latest")

executor = Executor()

"""
Create the flask app register the blueprints, 
and initialize the executor.
"""
def create_app(config="config.Development"):
    from views.home import home
    from views.auth import auth
    from views.contract_functions import contract_functions
    import auth as lm

    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(contract_functions)
    lm.init_login_manager(app)
    executor.init_app(app)

    @app.before_first_request
    def before_first_request():
        listen_for_events.submit()

    return app


"""
Thread that listens for events on the blockchain.
"""
@executor.job
def listen_for_events():
    from app import event_filter
    from flask import session
    i = 0
    #while True:
    #    i += 1
    #    session["event_count"] = i
    #    #print(event_filter.get_new_entries())
    #    #print(event_filter.get_all_entries())
    #    sleep(10)


if __name__ == "__main__":
    app = create_app(config=Development)
    app.run(debug=True)
