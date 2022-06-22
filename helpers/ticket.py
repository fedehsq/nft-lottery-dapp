class Ticket:
    """
    Class representation of a ticket.
    """
    def __init__(self, buyer: str, one: int, two: int, three: int, four: int, five: int, powerball: int):
        self.buyer = buyer
        self.one = one
        self.two = two
        self.three = three
        self.four = four
        self.five = five
        self.powerball = powerball