import json
from flask_login import current_user

class ContractProcessor:

    @staticmethod
    def deploy_contract(contract_name, *constructor_args):
        from app import w3, owner
        # compile your smart contract with truffle first
        truffle_file = json.load(open('./build/contracts/' + contract_name + '.json'))
        abi = truffle_file['abi']
        bytecode = truffle_file['bytecode']

        # Initialize a contract object with the smart contract compiled artifacts
        contract = w3.eth.contract(bytecode=bytecode, abi=abi)

        # build a transaction by invoking the buildTransaction() method from the smart contract constructor function
        construct_txn = contract.constructor(*constructor_args).buildTransaction({
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
        print(contract_address)

        # Initialize a contract instance object using the contract address which can be used to invoke contract functions
        contract_instance = w3.eth.contract(abi=abi, address=contract_address)
        return contract_address, contract_instance

    """
    Mint a collectible
    """
    @staticmethod
    def mint(id: int, collectible: str):
        from app import w3, lottery_instance
        try:
            tx = ContractProcessor.create_transaction()
            tx_hash = lottery_instance.functions.mint(int(id), collectible).transact(
                tx
            )
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print(tx_receipt)
            return tx_receipt['status']
        except Exception:
            return 0

    """
    Transfer a token from one address to another
    """
    @staticmethod
    def transfer_from(_from: str, to: str, token_id: int):
        from app import w3, nft_instance
        try:
            tx = ContractProcessor.create_transaction()
            tx_hash = nft_instance.functions.transferFrom(
                _from, to, int(token_id)
            ).transact(tx)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print(tx_receipt)
            return tx_receipt['status']
        except Exception as e:
            return 0

    """
    Create a transaction object in the format required by the web3.py library
    """
    @staticmethod
    def create_transaction():
        from app import w3, lottery_address
        wei = w3.toWei(10, "ether")
        tx = {
            "from": current_user.id,
            "to": lottery_address,
            "value": wei,
            "gas": 2000000,
            "gasPrice": w3.toWei("40", "gwei"),
        }
        return tx