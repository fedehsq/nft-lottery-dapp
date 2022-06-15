import json
from web3 import Web3, HTTPProvider
from flask import Flask

# create a web3.py instance w3 by connecting to the local Ethereum node
w3 = Web3(HTTPProvider("http://localhost:8545"))

# Initialize a local account object from the private key of a valid Ethereum node address
owner = w3.eth.account.from_key("0x46818ea21b18213658f826b612d7bddf01e7cf07a7c30018e89e3a3dcb816bed")

def deploy_contract(contract_name):
    # compile your smart contract with truffle first
    truffleFile = json.load(open('./build/contracts/' + contract_name + '.json'))
    abi = truffleFile['abi']
    bytecode = truffleFile['bytecode']

    # Initialize a contract object with the smart contract compiled artifacts
    contract = w3.eth.contract(bytecode=bytecode, abi=abi)

    # build a transaction by invoking the buildTransaction() method from the smart contract constructor function
    construct_txn = contract.constructor(3000, '0xb95A8c720bbDD408f97CccF07de6ceD493bDbc74').buildTransaction({
        'from': owner.address,
        'nonce': w3.eth.getTransactionCount(owner.address),
        'gas': 1728712,
        'gasPrice': w3.toWei('21', 'gwei')})

    # sign the deployment transaction with the private key
    signed = w3.eth.account.sign_transaction(construct_txn, owner.key)

    # broadcast the signed transaction to your local network using sendRawTransaction() method and get the transaction hash
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)

    # collect the Transaction Receipt with contract address when the transaction is mined on the network
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print("Contract Deployed At:", tx_receipt['contractAddress'])
    contract_address = tx_receipt['contractAddress']

    # Initialize a contract instance object using the contract address which can be used to invoke contract functions
    contract_instance = w3.eth.contract(abi=abi, address=contract_address)
    return contract_address, contract_instance

nft_address, nft_instance = deploy_contract('NFT')


def create_app(config="config.Development"):
    from views.home import home
    from views.auth import auth
    import auth as lm
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(home)
    app.register_blueprint(auth)
    lm.init_login_manager(app)
    return app

if __name__ == '__main__':
    from config import Development
    app = create_app(config=Development)
    app.run(debug=True)