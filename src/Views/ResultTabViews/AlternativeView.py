from tkinter import Canvas

class AlternativeView():
    """
    This class allows to represent an alternative on a schema. It takes the form of a circle with the name of the alternative

    Attributes
    ----------
    name : str
        the alternative name
    x : int
        the x coordinate of the center of the circle
    y : int
        the y coordinate of the center of the circle
    row : int
        the row of the circle on the graph
    column : int
        the column of the circle on the graph

    Methods
    -------
    getCoords()
        return (x, y), the coordinates of the center of the circle
    getRow()
        return the row of the circle on the graph
    getColumn()
        return the column of the circle on the graph
    """

    def __init__(self, name:str, canvas:Canvas, x:int, y:int, radius:int, row:int, column:int):
        """
        Parameters
        ----------
        name : str
            the alternative name
        canvas : Canavas
            the canvas where the alternative is drawed
        x : int
            the x coordinate of the center of the circle that represents the alternative
        y : int
            the y coordinate of the center of the circle that represents the alternative
        radius : int 
            the circle radius
        row : int 
            the row of the alternative on the graph
        column : int 
            the column of the alternative on the graph
        """

        self.name = name
        self.x = x
        self.y = y
        self.row = row
        self.column = column
        canvas.create_oval(x-radius, y-radius, x+radius, y+radius)
        canvas.create_text(x, y, text=self.name)

    
    def getCoords(self) -> tuple:
        """return (x, y), the coordinates of the center of the circle

        Return
        ------
        (x, y) : tuple(int,int)
            the coordinates of the center of the circle
        """

        return (self.x, self.y)
    

    def getRow(self):
        """return the row of the circle on the graph

        Return
        ------
        row : int
            the row of the circle on the graph
        """

        return self.row
    

    def getColumn(self):
        """return the column of the circle on the graph

        Return
        ------
        column : int
            the column of the circle on the graph
        """
        
        return self.column