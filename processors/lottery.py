from time import sleep
from flask_login import current_user
from processors.contract import ContractProcessor
from app import w3, manager, executor


class LotteryProcessor:

    # Filter for Lottery create event
    lottery_created_event = None

    # Filter for Lottery open round event
    round_opened_event = None

    # Filter for Lottery close event
    lottery_closed_event = None

    # Filter for Lottery draw winning numbers event
    winning_numbers_drawn_event = None

    # Filter for Lottery assign prize event
    prize_assigned = None

    # Filter for Lottery mint token event
    token_minted = None

    @staticmethod
    @executor.job
    def init_filters():

        """
        Initialize all the filters for the Lottery contract when the contract is deployed.
        Otherwise, the filters will be initialized when the contract is deployed.
        """
        while True:
            if ContractProcessor.LOTTERY_DEPLOYED:
                LotteryProcessor.lottery_created_event = (
                    ContractProcessor.lottery_instance.events.LotteryCreated.createFilter(
                        fromBlock=1, toBlock="latest"
                    )
                )
                LotteryProcessor.round_opened_event = (
                    ContractProcessor.lottery_instance.events.RoundOpened.createFilter(
                        fromBlock=1, toBlock="latest"
                    )
                )
                LotteryProcessor.lottery_closed_event = (
                    ContractProcessor.lottery_instance.events.LotteryClosed.createFilter(
                        fromBlock=1, toBlock="latest"
                    )
                )
                LotteryProcessor.winning_numbers_drawn_event = (
                    ContractProcessor.lottery_instance.events.WinningNumbersDrawn.createFilter(
                        fromBlock=1, toBlock="latest"
                    )
                )
                LotteryProcessor.prize_assigned = (
                    ContractProcessor.lottery_instance.events.PrizeAssigned.createFilter(
                        fromBlock=1, toBlock="latest"
                    )
                )
                LotteryProcessor.token_minted = (
                    ContractProcessor.lottery_instance.events.TokenMinted.createFilter(
                        fromBlock=1, toBlock="latest"
                    )
                )
                break
            else:
                sleep(10)

    @staticmethod
    def is_open():
        """
        :return: True if the lottery is open, False otherwise
        """

        return ContractProcessor.lottery_instance.functions.isLotteryActive().call()

    @staticmethod
    def is_already_minted(id: int):
        """
        :param id: id of the collectible
        :return: True if the collectible is already minted, False otherwise
        """
        return (
            ContractProcessor.nft_instance.functions.ownerOf(id).call() != ContractProcessor.ADDRESS_ZERO
        )

    @staticmethod
    def is_round_active():
        """
        :return: True if the round is active, False otherwise
        """

        return ContractProcessor.lottery_instance.functions.isRoundActive().call()

    @staticmethod
    def is_round_finished():
        """
        :return: True if the round is finished, False otherwise
        """

        return ContractProcessor.lottery_instance.functions.isRoundFinished().call()

    @staticmethod
    def is_winning_ticket_extracted():
        """
        :return: True if the winning ticket is already extracted, False otherwise
        """

        return ContractProcessor.lottery_instance.functions.areNumbersDrawn().call()

    @staticmethod
    def mint(id: int, collectible: str, rank: int):
        """
        Mint a collectible
        :param id: id of the collectible
        :param collectible: collectible name
        :param rank: rank of the collectible
        :return: Transaction result
        """
        try:
            tx = ContractProcessor.create_transaction(
                manager.address, ContractProcessor.lottery_address, 0
            )
            tx_hash = ContractProcessor.lottery_instance.functions.mint(
                id, rank, collectible
            ).transact(tx)
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
        try:
            tx = ContractProcessor.create_transaction(
                current_user.id, ContractProcessor.lottery_address, 1
            )
            tx_hash = ContractProcessor.lottery_instance.functions.buy(
                one, two, three, four, five, powerball
            ).transact(tx)
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
        try:
            tx = ContractProcessor.create_transaction(
                manager.address, ContractProcessor.lottery_address, 0
            )
            tx_hash = ContractProcessor.lottery_instance.functions.openRound().transact(
                tx
            )
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
        try:
            tx = ContractProcessor.create_transaction(
                manager.address, ContractProcessor.lottery_address, 0
            )
            tx_hash = (
                ContractProcessor.lottery_instance.functions.closeLottery().transact(tx)
            )
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
        try:
            tx = ContractProcessor.create_transaction(
                manager.address, ContractProcessor.lottery_address, 0
            )
            tx_hash = (
                ContractProcessor.lottery_instance.functions.drawNumbers().transact(tx)
            )
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
        try:
            tx = ContractProcessor.create_transaction(
                manager.address, ContractProcessor.lottery_address, 0
            )
            tx_hash = (
                ContractProcessor.lottery_instance.functions.givePrizes().transact(tx)
            )
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            print(tx_receipt)
            return tx_receipt["status"]
        except Exception as e:
            print(e)
            return 0
