from customtkinter import (CTkButton, CTkLabel)
from Tabular import Tabular
from Controllers.DataTabController import DataTabController

class DataTabView:
    def __init__(self, master) -> None:
        self.master = master
        self.ctkb1 = CTkButton(master=self.master, text="Open a file", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.open_file)
        self.ctkb1.pack(side="top", pady=10)
        
        self.ctklabel_data_note = CTkLabel(self.master, text="Only csv files are accepted", fg_color="#ffffff", text_color="#000000", corner_radius=5)
        self.ctklabel_data_note.pack(side="top")

        # TODO
        # tabular
        #self.tabular = Tabular(master=self.master, x=50, y=125)

        self.controller = DataTabController()


    def open_file(self) -> None:
        if self.controller:
            self.controller.open_file()