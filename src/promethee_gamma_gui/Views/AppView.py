from customtkinter import (CTk, CTkTabview, CTkButton, CTkFrame)
from ..Resources.Menu import Menu

class AppView(CTk):
    """
    A class to handle the view of the PROMETHEE Gamma GUI application

    Attributes
    ----------
    Menuframe : CTkFrame
        a frame to display menus
    menu : Menu
        a drop down menu to select action (new, load, save, save as)
    help : Menu
        a drop-down menu to select the help
    aboutButton : CTkButton
        a button to display the "about" view
    quitbutton : CTkButton
        a button to quit the app
    tabView : CTkTabView
        a tabView that will contain the 3 main tabs of the application
    dataTab : CTkFrame
        the data tab, first tab of the application
    resultTab : CTkFrame
        the result tab, second tab of the application
    helpForParametersTab : CTkFrame
        the help For Parameters tab, third tab of the application
    listener : AppView.ViewListener
        the listener of this view
    """

    class ViewListener:
        """
        An interface for the listener of this class
        """

        def menuChoice(self, choice:str):
            """Handle the choice made by the user in the Project menu

            Parameters
            ----------
            choice : str
                the choice made by the user. It can be "new", "save as", "save" or "load"
            """
            pass

        def menuHelp(self, choice:str):
            """Show the help corresponding to choice

            Parameters
            ----------
            choice : str
                the choice made by the user. 
                It can be "Data", "Parameters", "Matrix", "Orthogonal graph", "Rank graph", "Preference learning" or "Custom"
            """
            pass

        def about(self):
            """Show about window
            """
            pass

        def quit(self):
            """Quit the app
            """
            pass


    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.geometry("820x750")
        self.configure(cursor="arrow")
        self.minsize(820, 750)
        self.resizable(True, True)
        self.title("Promethee Gamma")


        self.MenuFrame = CTkFrame(self, height=28)
        self.menu = Menu(master=self.MenuFrame, text="Project", command=self.menuChoice, values=["new", "load", "save", "save as"], width=80)
        self.help = Menu(master=self.MenuFrame, text="Help", command=self.menuHelp, width=80,
                         values=["Data", "Parameters", "Matrix", "Orthogonal graph", "Rank graph", "Preference learning", "Custom"])
        self.aboutButton = CTkButton(master=self.MenuFrame, text="About", command=self.about, width=80)
        self.quitButton = CTkButton(master=self.MenuFrame, text="Quit", command=self.clickOnQuit, width=80)

        self.tabview = CTkTabview(self, fg_color="#ffffff")
        self.dataTab = self.tabview.add("Data")
        self.dataTab.configure(border_color="#000080", corner_radius=5, fg_color="#ffffff")

        self.resultTab = self.tabview.add("Results")
        self.resultTab.configure(border_color="#000080", corner_radius=5, fg_color="#ffffff")

        self.helpForParametersTab = self.tabview.add("Help for Parameters")
        self.resultTab.configure(border_color="#000080", corner_radius=5, fg_color="#ffffff")

        self.listener = None


    def setListener(self, l:ViewListener):
        """Set the listener

        Parameters
        ----------
        l : ViewListener
            the new listener
        """
        self.listener = l


    def show(self):
        """Show the app
        """
        self.MenuFrame.pack(side="top", fill="x", pady=0, ipady=0)
        self.menu.pack(anchor="nw", side="left", pady=0, ipady=0, padx=1)
        self.help.pack(anchor="nw", side="left", pady=0, ipady=0,padx=1)
        self.aboutButton.pack(anchor="nw", side="left", pady=0, ipady=0,padx=1)
        self.quitButton.pack(anchor="nw", side="left", pady=0, ipady=0,padx=1)
        self.tabview.pack(side="top", expand=True, fill="both", pady=0, ipady=0)
        

    def getTabs(self):
        """Return the 3 tabs of the app

        Returns
        -------
        a tuple of 3 CTkFrame
            the 3 tabs of the app
        """
        return (self.dataTab, self.resultTab, self.helpForParametersTab)
    

    def setTab(self, name:str):
        """Set the focus on the tab of name "name"

        name : str
            the name of the tab that will receive the focus
        """
        self.tabview.set(name)


    def menuChoice(self, choice:str):
        """Handle selection in project menu
        """
        self.listener.menuChoice(choice)


    def menuHelp(self, choice:str):
        """Handle selection in help menu
        """
        self.listener.menuHelp(choice)


    def about(self):
        """Handle click on quit button
        """
        self.listener.about()


    def clickOnQuit(self):
        """Handle click on quit button
        """
        self.listener.quit()