class NftCollectible:
    def __init__(self, id: int, collectible: str, owner="0x0000000000000000000000000000000000000000"):
        self.id = id
        self.collectible = collectible
        self.owner = owner

    def __repr__(self):
        return f"{self.id} {self.collectible} {self.owner}"