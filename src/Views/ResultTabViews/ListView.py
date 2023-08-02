from customtkinter import (CTkCheckBox)

class ListView:
    class ViewListener:
        def checkBoxEvent(self):
            pass


    def __init__(self, master, alternatives:list) -> None:
        self.master = master
        self.listener = None
        self.alternatives = alternatives
        self.CheckBoxList = []


    def setListener(self, l:ViewListener):
        self.listener = l


    def build(self):
        for a in self.alternatives:
            c = CTkCheckBox(master=self.master, text=a.getName(), variable=a.getVar(), command=self.checkbox_event)
            self.CheckBoxList.append(c)


    def show(self):
        a = 0
        r = 0
        for c in self.CheckBoxList:
            c.grid(row=r, column=a, sticky="n", padx=20, pady=(5, 0))
            if a == 0:
                a = 1
            else:
                a = 0
                r += 1


    def checkbox_event(self):
        self.listener.checkBoxEvent()
