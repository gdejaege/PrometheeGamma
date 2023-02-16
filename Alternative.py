from tkinter import Canvas

class Alternative():
    """
    This class allows to represent an alternative on a schema. It takes the form of a circle with the name of the alternative
    """
    def __init__(self, n:str, m:Canvas, x, y):
        self.name = n
        self.x = x
        self.y = y
        m.create_oval(x-30, y-30, x+30, y+30)
        m.create_text(x, y, text=n)

    
    def get_coords(self) -> tuple:
        """
        return (x, y) the coordinates of the alternative
        """
        return (self.x, self.y)