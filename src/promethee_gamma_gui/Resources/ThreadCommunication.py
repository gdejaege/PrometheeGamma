from enum import Enum, auto

"""
These 2 classes are taken from the youtube tutorial that can be found at the following address:
https://www.youtube.com/watch?v=ghSDvtVJPck
"""

class TicketPurpose(Enum):
    """
    An Enum class for ticket purpose in thread communication
    """
    CANVAS_DRAW = auto()
    MATPLOTLIB_AX_PLOT = auto()
    MATPLOTLIB_AX_ADD_PATCH = auto()



class Ticket:
    """
    A class to create a ticket for thread communication
    """
    def __init__(self, ticketType:TicketPurpose, ticketValue:any):
        try:
            self.ticketType = ticketType
            self.ticketValue = ticketValue
        except SystemExit:
            raise SystemExit()
