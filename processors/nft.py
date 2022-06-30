from processors.contract import ContractProcessor


class NftProcessor:
    """
    This class is used to process the NFT data.
    """

    @staticmethod
    def owner_of(id: int):
        """
        Get the owner of a id collectible.
        :param id: id of the collectible
        :return: owner of the collectible
        """
        return ContractProcessor.nft_instance.functions.ownerOf(id).call()

    @staticmethod
    def balance_of(address: str):
        """
        Get the balance of an address.
        :param address: address
        :return: balance of the address
        """
        return ContractProcessor.nft_instance.functions.balanceOf(address).call()

    # @staticmethod
    # def transfer_from(_from: str, to: str, token_id: int):
    #    """
    #    Transfer a token from one address to another
    #    """
    #    from app import w3, nft_instance
    #    try:
    #        tx = ContractProcessor.create_transaction()
    #        tx_hash = nft_instance.functions.transferFrom(
    #            _from, to, int(token_id)
    #        ).transact(tx)
    #        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    #        print(tx_receipt)
    #        return tx_receipt['status']
    #    except Exception as e:
    #        return 0
