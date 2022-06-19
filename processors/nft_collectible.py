class NftCollectible:
    def __init__(self, id: int, collectible: str, rank: int, owner: str ):
        self.id = id
        self.collectible = collectible
        self.owner = owner
        self.rank = rank 

    def __repr__(self):
        return f"{self.id} {self.collectible} {self.owner}"