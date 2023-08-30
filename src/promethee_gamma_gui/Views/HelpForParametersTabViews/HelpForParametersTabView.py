from customtkinter import (CTkLabel, CTkButton, CTkRadioButton, IntVar, CTkFrame, CTkCanvas, CTkScrollbar, CTkScrollableFrame)

#from Models.DataTabModels.Alternative import Alternative
from ...Models.DataTabModels.Alternative import Alternative


class HelpForParametersTabView:
    """
    A class to display the starting content of the helpForParameters tab

    Attributes
    ----------
    sframe : ScrollableFrame
        the scrollableFrame
    master : CTkFrame
        the master frame
    startLabel : CTkLabel
        a label to display the strarting Text
    preferenceLearningButton : CTkButton
        a button to select the built-in preferenceLearning algorithm
    row : int
        the row for positionning elements with grid method
    listener : ViewListener
        the listener of this view
    """

    class ViewListener:
        """
        An interface for the listener of this view
        """

        def showPreferenceLearning(self):
            """Show the preference learning view
            """
            pass

        def showCustom(self):
            """Show the custom view
            """
            pass


    def __init__(self, master) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the parent master frame
        """
        self.master = master
        startText = "Please choose a method. The preference learning button will launch the application's built-in preference learning algorithm. The custom button will load the Custom module."
        self.startLabel = CTkLabel(master=self.master, text=startText, text_color="#000000", wraplength=580)
        self.preferenceLearningButton = CTkButton(master=self.master, text="Preference learning", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.startPreferenceLearning)
        self.customButton = CTkButton(master=self.master, text="Custom", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.startCustom)
        self.listener = None
        self.row = 0


    def setListener(self, l:ViewListener):
        """Set the listener

        Parameters
        ----------
        l : ViewListener
            the new listener
        """
        self.listener = l


    def getMaster(self):
        """Return the master frame of the tab

        Return
        ------
        master : CTkFrame
            the master frame
        """
        return self.master


    def show(self):
        """Show the view
        """
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        self.startLabel.grid(row=self.row, column=0, columnspan=2, padx=10, pady=(20, 0), sticky="n")
        self.row +=1
        self.preferenceLearningButton.grid(row=self.row, column=0, padx=10, pady=(20, 0), sticky="ne")
        self.customButton.grid(row=self.row, column=1, padx=10, pady=(20, 0), sticky="nw")


    def hide(self):
        """Hide the view
        """
        self.row -= 1
        self.startLabel.destroy()
        self.preferenceLearningButton.destroy()
        self.customButton.destroy()
        self.master.grid_columnconfigure(1, weight=0)


    def restart(self):
        """Reinitialize the variables for display

        They can be destroy in Custom module, so, for stability, we redifine them.
        """
        for w in self.master.winfo_children():
            w.destroy()

        startText = "Please choose a method. The preference learning button will launch the application's built-in preference learning algorithm. The custom button will load the Custom module."
        self.startLabel = CTkLabel(master=self.master, text=startText, text_color="#000000", wraplength=580)
        self.preferenceLearningButton = CTkButton(master=self.master, text="Preference learning", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.startPreferenceLearning)
        self.customButton = CTkButton(master=self.master, text="Custom", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.startCustom)


    def startPreferenceLearning(self):
        """Start the preference learning method
        """
        self.listener.showPreferenceLearning()


    def startCustom(self):
        """Start the custom method
        """
        self.listener.showCustom()
