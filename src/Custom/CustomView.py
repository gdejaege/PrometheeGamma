#############################################################################
### This class is a skeleton designed to display an alternative way       ###
### of obtaining parameter values specific to the PROMETHEE Gamma method. ###
### Edit it as you wish.                                                  ###
#############################################################################

from customtkinter import (CTkButton) # Import what you need

class CustomView:
    """
    A class to display custom component of the custom module

    Attributes
    ----------
    master : CTkFRame
        the master frame
    listener : ViewListener
        the listener of this view
    quitButton : CTkButton
        the quit button, to quit the custom module

    Methods
    -------
    setListener(l:ViewListener)
        set the listener
    show(self):
        show the custom components
    quit(self):
        handle click on quitButton
    """

    class ViewListener:
        """
        An interface for the listener of this view

        Methods
        -------
        reset()
            reset the tab content
        """

        def reset(self):
            pass

        # Add your methods if needed


    def __init__(self, master) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the master frame
        """
        self.master = master
        self.listener = None

        # You can write code here to create all component that you need to display on the tab

        self.quitButton = CTkButton(master=self.master, text="Quit", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.quit)


    def setListener(self, l:ViewListener):
        """Set the listener

        Parameters
        ----------
        l : ViewListener
            the new listener
        """
        self.listener = l


    def show(self):
        """Show the custom components
        """
        
        # You can write code here to display all component that you created

        self.quitButton.grid(row=10, column=0, padx=10, pady=(10,0), sticky="n")


    def quit(self):
        """Handle click on quitButton
        """
        self.listener.reset()


    # Add your methods if needed

