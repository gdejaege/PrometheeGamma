from customtkinter import CTkTextbox
import time

class DisplayMatrixResultsView:
    """
    A class to display the matrixResults in a textbox

    Attributes
    ----------
    textboxResults : CTkTexbox
        a textbox that will contain the matrixResults

    Methods
    -------
    show(matrixResults:list)
        Show the matrixResults in a textbox
    refresh(matrixResults:list)
        Refresh the textbox
    _print_(matrixResults:list)
        Delete previous content and then print the matrixResults in the textbox
    """

    def __init__(self, master) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the master frame
        """

        self.texbox_results = CTkTextbox(master=master, text_color="#000000", fg_color="#ffffff", wrap='word')


    def show(self, matrixResults:list):
        """Show the matrixResults in a textbox

        Parameters
        ----------
        matrixResults : list
            the matrixResults to display
        """

        self.texbox_results.pack(expand=True, fill='both')
        self._print_(matrixResults)

        """
        for i in range(10):
            print("res", i)
            time.sleep(1)
        """


    def refresh(self, matrixResults:list):
        """Refresh the textbox

        Parameters
        ----------
        matrixResults : list
            the new matrixResults to display
        """
        self._print_(matrixResults)

    
    def _print_(self, matrixResults:list):
        """Delete previous content and then dispay new content in the textbox

        Parameters
        ----------
        matrixResults : list
            the new matrixResults to display
        """
        self.texbox_results.delete("1.0", "end")
        for i in range(len(matrixResults)):
            line = ""
            for e in matrixResults[i]:
                line += str(e) + ", "
            self.texbox_results.insert("end", line+"\n")