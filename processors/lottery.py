from processors.contract import ContractProcessor


class LotteryProcessor:
    @staticmethod
    def mint(id: int, collectible: str, rank: int):
        """
        Mint a collectible
        :param id: id of the collectible
        :param collectible: collectible name
        :param rank: rank of the collectible
        :return: Transaction result
        """
        from app import w3, lottery_instance, lottery_address, manager

        try:
            tx = ContractProcessor.create_transaction(
                manager.address, lottery_address, 0
            )
            tx_hash = lottery_instance.functions.mint(id, rank, collectible).transact(
                tx
            )
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print(tx_receipt)
            return tx_receipt["status"]
        except Exception as e:
            print(e)
            return 0
