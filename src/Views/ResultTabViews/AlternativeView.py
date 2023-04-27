from tkinter import Canvas

class AlternativeView():
    """
    This class allows to represent an alternative on a schema. It takes the form of a circle with the name of the alternative
    """
    def __init__(self, name:str, canvas:Canvas, x, y):
        self.name = name
        self.x = x
        self.y = y
        canvas.create_oval(x-30, y-30, x+30, y+30)
        canvas.create_text(x, y, text=self.name)

    
    def get_coords(self) -> tuple:
        """
        return (x, y) the coordinates of the alternative
        """
        return (self.x, self.y)