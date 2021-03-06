import json


class ContractProcessor:
    """
    This class is used to process the contract generic calls.
    """

    ADDRESS_ZERO = "0x0000000000000000000000000000000000000000"
    LOTTERY_DEPLOYED = False
    ROUND_DURATION = 2

    nft_address = None
    nft_instance = None

    lottery_address = None
    lottery_instance = None

    @staticmethod
    def deploy_contract(contract_name, *constructor_args):
        """
        This method is used to deploy a contract.
        :param contract_name: Name of the contract to deploy.
        :param constructor_args: Arguments to pass to the contract constructor.
        :return: The address of the contract and the contract instance.
        """
        from app import w3, manager

        truffle_file = json.load(open("./build/contracts/" + contract_name + ".json"))
        abi = truffle_file["abi"]
        bytecode = truffle_file["bytecode"]

        # Initialize a contract object with the smart contract compiled artifacts
        contract = w3.eth.contract(bytecode=bytecode, abi=abi)

        # build a transaction by invoking the buildTransaction() method from the smart contract constructor function
        construct_txn = contract.constructor(*constructor_args).buildTransaction(
            {
                "from": manager.address,
                "nonce": w3.eth.getTransactionCount(manager.address),
                "gas": 30000000,
                "gasPrice": w3.toWei("21", "gwei"),
            }
        )

        # sign the deployment transaction with the private key
        signed = w3.eth.account.sign_transaction(construct_txn, manager.key)

        # broadcast the signed transaction to your local network using sendRawTransaction() method and get the transaction hash
        tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)

        # collect the Transaction Receipt with contract address when the transaction is mined on the network
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        contract_address = tx_receipt["contractAddress"]

        # Initialize a contract instance object using the contract address which can be used to invoke contract functions
        contract_instance = w3.eth.contract(abi=abi, address=contract_address)
        return contract_address, contract_instance

    @staticmethod
    def deploy_contracts():
        # Nft contract address and ABI
        (
            ContractProcessor.nft_address,
            ContractProcessor.nft_instance,
        ) = ContractProcessor.deploy_contract("NFT")

        # Lottery contract address and ABI (pass Nft contract address as parameter)
        (
            ContractProcessor.lottery_address,
            ContractProcessor.lottery_instance,
        ) = ContractProcessor.deploy_contract(
            "Lottery", ContractProcessor.nft_address, ContractProcessor.ROUND_DURATION
        )
        if (
            ContractProcessor.lottery_address is not None
            and ContractProcessor.lottery_instance is not None
            and ContractProcessor.nft_address is not None
            and ContractProcessor.nft_instance is not None
        ):
            ContractProcessor.LOTTERY_DEPLOYED = True
            return True
        return False

        # Initialize the lottery filters for the events
        # LotteryProcessor.init_filters()

    @staticmethod
    def create_transaction(_from: str, _to: str, _value: int):
        """
        Create a transaction object in the format required by the web3.py library
        :param _from: Address from which the transaction is sent.
        :param _to: Address to which the transaction is sent.
        :param _value: Amount of ether to send.
        :return: A transaction object.
        """
        from app import w3

        wei = w3.toWei(_value, "ether")
        tx = {
            "from": _from,
            "to": _to,
            "value": wei,
            "gas": 2618850,
            "gasPrice": w3.toWei("40", "gwei"),
        }
        return tx
