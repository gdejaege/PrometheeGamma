from customtkinter import (CTk, CTkTabview)

class AppView(CTk):
    
    class ViewListener:
        def showDataTabView(self, master):
            pass
        def showResultTabView(self, master):
            pass
        def showHelpForParametersTabView(self, master):
            pass


    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.listener = None

        self.geometry("500x500")
        self.configure(cursor="arrow")
        #self.maxsize(5000, 5000)
        self.minsize(500, 500)
        self.resizable(True, True)
        self.title("Promethee Gamma")


    def setListener(self, listener:ViewListener):
        self.listener = listener


    def show(self):
        self.tabview = CTkTabview(self, fg_color="#ffffff")
        self.tabview.pack(expand=True, fill="both")
        self.dataTab = self.tabview.add("Data")
        self.dataTab.configure(
            #background="#000000",
            #bg_color="#000080",
            border_color="#000080",
            corner_radius=5,
            cursor="arrow",
            fg_color="#ffffff")
        self.listener.showDataTabView(master=self.dataTab)

        self.resultTab = self.tabview.add("Results")
        self.resultTab.configure(
            #background="#000000",
            #bg_color="#000080",
            border_color="#000080",
            corner_radius=5,
            fg_color="#ffffff")
        self.listener.showResultTabView(master=self.resultTab)

        self.helpForParametersTab = self.tabview.add("Help for Parameters")
        self.resultTab.configure(
            #background="#000000",
            #bg_color="#000080",
            border_color="#000080",
            corner_radius=5,
            fg_color="#ffffff")
        self.listener.showHelpForParametersTabView(master=self.helpForParametersTab)


