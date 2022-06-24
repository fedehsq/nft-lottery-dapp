from flask_login import current_user
from processors.contract import ContractProcessor


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
    def init_filters():
        from app import lottery_instance
        """
        Initialize all the filters for the Lottery contract.
        """
        LotteryProcessor.lottery_created_event = lottery_instance.events.LotteryCreated.createFilter(
            fromBlock=1, toBlock="latest"
        )
        LotteryProcessor.round_opened_event = lottery_instance.events.RoundOpened.createFilter(
            fromBlock=1, toBlock="latest"
        )
        LotteryProcessor.lottery_closed_event = lottery_instance.events.LotteryClosed.createFilter(
            fromBlock=1, toBlock="latest"
        )
        LotteryProcessor.winning_numbers_drawn_event = lottery_instance.events.WinningNumbersDrawn.createFilter(
            fromBlock=1, toBlock="latest"
        )
        LotteryProcessor.prize_assigned = lottery_instance.events.PrizeAssigned.createFilter(
            fromBlock=1, toBlock="latest"
        )
        LotteryProcessor.token_minted = lottery_instance.events.TokenMinted.createFilter(
            fromBlock=1, toBlock="latest"
        )


    @staticmethod
    def is_open():
        """
        :return: True if the lottery is open, False otherwise
        """
        from app import lottery_instance
        return lottery_instance.functions.isLotteryActive().call()
    
    @staticmethod
    def is_already_minted(id: int):
        """
        :param id: id of the collectible
        :return: True if the collectible is already minted, False otherwise
        """
        from app import nft_instance
        return nft_instance.functions.ownerOf(id).call() != ContractProcessor.ADDRESS_ZERO
    
    @staticmethod
    def is_round_active():
        """
        :return: True if the round is active, False otherwise
        """
        from app import lottery_instance
        return lottery_instance.functions.isRoundActive().call()
    
    @staticmethod
    def is_round_finished():
        """
        :return: True if the round is finished, False otherwise
        """
        from app import lottery_instance
        return lottery_instance.functions.isRoundFinished().call()

    @staticmethod
    def is_winning_ticket_extracted():
        """
        :return: True if the winning ticket is already extracted, False otherwise
        """
        from app import lottery_instance
        return lottery_instance.functions.areNumbersDrawn().call()

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
        from app import w3, lottery_instance, lottery_address
        # 

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
