import tkinter.messagebox as msg

from Resources.Reader import Reader


class HelpController:
    """
    A class to control help display

    Attributes
    ----------
    files : dict
        the dictionnary of resource files in which help is stored
    """
    def __init__(self) -> None:
        self.files = {"Data":"./Files/helpData.txt", 
                 "Parameters":"./Files/helpParameters.txt", 
                 "Matrix":"./Files/helpMatrix.txt", 
                 "Orthogonal graph":"./Files/helpOrthogonalGraph.txt", 
                 "Rank graph":"./Files/helpRankGraph.txt", 
                 "Preference learning":"./Files/helpPreferenceLearning.txt", 
                 "Custom":"./Files/helpCustom.txt"}
        

    def show(self, choice:str):
        """Show the help corresponding to choice

        Parameters
        ----------
        choice : str
            the choice made by the user. 
            It can be "Data", "Parameters", "Matrix", "Orthogonal graph", "Rank graph", "Preference learning" or "Custom"
        """
        try:
            r = Reader()
            text = r.readTxt(self.files[choice])
        except FileNotFoundError:
            msg.showerror("Error", "The resource could not be loaded, a file is missing.")
            return
        
        msg.showinfo("Help " + choice, text)