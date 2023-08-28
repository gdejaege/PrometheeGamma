from customtkinter import (CTk, CTkTabview, CTkButton, CTkFrame)
from Resources.Menu import Menu

class AppView(CTk):
    """
    A class to handle the view of the PROMETHEE Gamma GUI application

    Attributes
    ----------
    tabView : CTkTabView
        a tabView that will contain the 3 main tabs of the application
    dataTab : CTkFrame
        the data tab, first tab of the application
    resultTab : CTkFrame
        the result tab, second tab of the application
    helpForParametersTab : CTkFrame
        the help For Parameters tab, third tab of the application

    Methods
    -------
    show()
        show the app
    getTabs()
        return the 3 tabs of the app
    """

    class ViewListener:
        def menuChoice(self, choice:str):
            pass
        def menuHelp(self, choice:str):
            pass
        def about(self):
            pass
        def quit(self):
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
        self.listener = l


    def show(self):
        """Show the app
        """
        """
        self.menu.place(x=0,y=0,anchor="nw")
        self.aboutButton.place(x=80,y=0,anchor="nw")
        self.quitButton.place(x=160,y=0,anchor="nw")
        self.tabview.place(x=0,y=28,relwidth=1.0, height=self.winfo_height()-28)
        """
        self.MenuFrame.pack(side="top", fill="x", pady=0, ipady=0)
        self.menu.pack(anchor="nw", side="left", pady=0, ipady=0, padx=1)
        self.help.pack(anchor="nw", side="left", pady=0, ipady=0,padx=1)
        self.aboutButton.pack(anchor="nw", side="left", pady=0, ipady=0,padx=1)
        self.quitButton.pack(anchor="nw", side="left", pady=0, ipady=0,padx=1)
        self.tabview.pack(side="top", expand=True, fill="both", pady=0, ipady=0)
        

    def getTabs(self):
        """Return the 3 tabs of the app

        Return
        ------
        (dataTab, resultTab, helpForParametersTab) : Tuple(CTkFrame, CTkFRame, CTkFrame)
            the 3 tabs of the app
        """
        return (self.dataTab, self.resultTab, self.helpForParametersTab)
    

    def setTab(self, name:str):
        self.tabview.set(name)


    def menuChoice(self, choice:str):
        self.listener.menuChoice(choice)


    def menuHelp(self, choice:str):
        self.listener.menuHelp(choice)


    def about(self):
        self.listener.about()


    def clickOnQuit(self):
        self.listener.quit()

