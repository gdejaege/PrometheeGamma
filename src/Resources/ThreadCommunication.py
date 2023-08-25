
from enum import Enum, auto

# https://www.youtube.com/watch?v=ghSDvtVJPck

class TicketPurpose(Enum):
    # data tab
    BUTTON_UNIT_GRID_CONFIGURE = auto()
    BUTTON_CRITERION_GRID_CONFIGURE = auto()
    PUT_ENTRY_ON_GRID = auto()


    # rank view
    CANVAS_DRAW = auto()
    MAKE_MATPLOTLIB_LEGEND = auto()
    MATPLOTLIB_AX_PLOT = auto()
    MATPLOTLIB_AX_ADD_PATCH = auto()
    TEST = auto()



class Ticket:
    def __init__(self, ticketType:TicketPurpose, ticketValue:any):
        self.ticketType = ticketType
        self.ticketValue = ticketValue
