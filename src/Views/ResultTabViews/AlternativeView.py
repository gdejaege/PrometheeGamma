from tkinter import Canvas

class AlternativeView():
    """
    This class allows to represent an alternative on a schema. It takes the form of a circle with the name of the alternative
    """
    def __init__(self, name:str, canvas:Canvas, x:int, y:int, radius:int, row:int, column:int):
        self.name = name
        self.x = x
        self.y = y
        self.row = row
        self.column = column
        canvas.create_oval(x-radius, y-radius, x+radius, y+radius)
        canvas.create_text(x, y, text=self.name)

    
    def get_coords(self) -> tuple:
        """
        return (x, y) the coordinates of the alternative
        """
        return (self.x, self.y)
    

    def getRow(self):
        return self.row
    

    def getColumn(self):
        return self.column