from flask_login import current_user
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

    @staticmethod
    def buy_ticket(
        one: int, two: int, three: int, four: int, five: int, powerball: int
    ):
        """
        Buy a ticket for the current user.
        :param one: first number
        :param two: second number
        :param three: third number
        :param four: fourth number
        :param five: fifth number
        :param powerball: powerball number
        :return: Transaction result
        """
        from app import w3, lottery_instance, lottery_address, manager

        try:
            tx = ContractProcessor.create_transaction(
                current_user.id, lottery_address, 1
            )
            tx_hash = lottery_instance.functions.buy(
                one, two, three, four, five, powerball
            ).transact(tx)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print(tx_receipt)
            return tx_receipt["status"]
        except Exception as e:
            print(e)
            return 0

    @staticmethod
    def create_lottery():
        """
        Create the lottery
        :return: Transaction result
        """
        from app import w3, lottery_instance, lottery_address, manager

        try:
            tx = ContractProcessor.create_transaction(
                manager.address, lottery_address, 0
            )
            tx_hash = lottery_instance.functions.createLottery().transact(tx)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print(tx_receipt)
            return tx_receipt["status"]
        except Exception as e:
            print(e)
            return 0

    @staticmethod
    def open_round():
        """
        Open the round
        :return: Transaction result
        """
        from app import w3, lottery_instance, lottery_address, manager

        try:
            tx = ContractProcessor.create_transaction(
                manager.address, lottery_address, 0
            )
            tx_hash = lottery_instance.functions.openRound().transact(tx)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print(tx_receipt)
            return tx_receipt["status"]
        except Exception as e:
            print(e)
            return 0

    @staticmethod
    def close_lottery():
        """
        Close the lottery
        :return: Transaction result
        """
        from app import w3, lottery_instance, lottery_address, manager

        try:
            tx = ContractProcessor.create_transaction(
                manager.address, lottery_address, 0
            )
            tx_hash = lottery_instance.functions.closeLottery().transact(tx)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print(tx_receipt)
            return tx_receipt["status"]
        except Exception as e:
            print(e)
            return 0

    @staticmethod
    def extract_winning_ticket():
        """
        Extract the winning ticket
        :return: Transaction result
        """
        from app import w3, lottery_instance, lottery_address, manager

        try:
            tx = ContractProcessor.create_transaction(
                manager.address, lottery_address, 0
            )
            tx_hash = lottery_instance.functions.drawNumbers().transact(tx)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print(tx_receipt)
            return tx_receipt["status"]
        except Exception as e:
            print(e)
            return 0

    @staticmethod
    def give_prizes():
        """
        Give the prizes
        :return: Transaction result
        """
        from app import w3, lottery_instance, lottery_address, manager

        try:
            tx = ContractProcessor.create_transaction(
                manager.address, lottery_address, 0
            )
            tx_hash = lottery_instance.functions.givePrizes().transact(tx)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print(tx_receipt)
            return tx_receipt["status"]
        except Exception as e:
            print(e)
            return 0
