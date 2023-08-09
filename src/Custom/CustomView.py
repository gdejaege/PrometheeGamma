from customtkinter import (CTkButton) # Import what you need

class CustomView:

    class ViewListener:
        """
        An interface for the listener of this view
        """

        def cancel(self):
            pass


    def __init__(self, master) -> None:
        self.master = master

        # TODO You can write code here to create all component that you need to display on the tab

        self.cancelButton = CTkButton(master=self.master, text="Cancel", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.cancel)


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
        
        # TODO You can write code here to display all component that you created

        self.cancelButton.grid(row=10, column=0, padx=10, pady=(10,0), sticky="n")


    def cancel(self):
        """Handle click on cancelButton
        """
        self.listener.cancel()

