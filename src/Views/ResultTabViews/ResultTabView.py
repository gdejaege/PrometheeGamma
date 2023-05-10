from customtkinter import (CTkLabel, DoubleVar, CTkEntry, CTkSlider, StringVar, CTkButton)

class ResultTabView:
    class ViewListener:
        def changeOnTi(self, newValue:float):
            pass
        def changeOnTj(self, newValue:float):
            pass
        def changeOnPf(self):
            pass
        def obtainResults(self):
            pass
        def loadResultsVisualisation(self, master):
            pass
    
    
    def __init__(self, master, Ti:DoubleVar, Tj:DoubleVar, Pf:DoubleVar) -> None:
        self.master = master
        self.listener = None
        
        # Parameters values
        self.Ti = Ti
        self.Tj = Tj
        self.Pf = Pf

        # Labels
        self.label_Ti = CTkLabel(master=self.master, text="Global indifference threshold (Ti):", text_color="#000000", justify="left", padx=10, pady=10)
        self.label_Tj = CTkLabel(master=self.master, text="Global incomparability threshold (Tj):", text_color="#000000", justify="left", padx=10, pady=10)
        self.label_Pf = CTkLabel(master=self.master, text="Global preference factor (Pf):", text_color="#000000", justify="left", padx=10, pady=10)
        
        #Entries
        self.entry_Ti = CTkEntry(master=self.master, textvariable=self.Ti, width=50)
        self.entry_Ti.bind("<Return>", command=self.commandEntryTi)
        self.entry_Tj = CTkEntry(master=self.master, textvariable=self.Tj, width=50)
        self.entry_Tj.bind("<Return>", command=self.commandEntryTj)
        self.entry_Pf = CTkEntry(master=self.master, textvariable=self.Pf, width=50)
        self.entry_Pf.bind("<Return>", command=self.commandEntryPf)
        
        # Sliders
        self.slider_Ti= CTkSlider(master=self.master, from_=0, to=1, number_of_steps=100, command=self.commandSliderTi)
        self.slider_Ti.set(output_value=self.Ti.get() ,from_variable_callback=True)
        self.slider_Tj= CTkSlider(master=self.master, from_=0, to=1, number_of_steps=100, command=self.commandSliderTj)
        self.slider_Tj.set(output_value=self.Tj.get() ,from_variable_callback=True)
        self.slider_Pf= CTkSlider(master=self.master, from_=1, to=100, number_of_steps=1000, command=self.commandSliderPf)
        self.slider_Pf.set(output_value=self.Pf.get() ,from_variable_callback=True)

        # Button
        self.textButtonObtainResults = StringVar(master=self.master, value="Obtain results")
        self.buttonObtainResults = CTkButton(self.master, textvariable=self.textButtonObtainResults, command=self.onClickButtonObtainResults, fg_color="#6cffff", text_color="#000000")


    def setListener(self, l:ViewListener) -> None:
        self.listener = l


    def show(self) -> None:
        self.label_Ti.place(x=10, y=10)
        self.label_Tj.place(x=10, y=40)
        self.label_Pf.place(x=10, y=70)
        
        self.entry_Ti.place(x=250, y=10)
        self.entry_Tj.place(x=250, y=40)
        self.entry_Pf.place(x=250, y=70)

        self.slider_Ti.place(x=310, y=15)
        self.slider_Tj.place(x=310, y=45)
        self.slider_Pf.place(x=310, y=75)

        self.buttonObtainResults.place(relx=0.5, y=120, anchor="center")


    def refresh(self):
        self.commandEntryTi(0)
        self.commandEntryTj(0)
        self.commandEntryPf(0)


    def commandEntryTi(self, event) -> None:
        """
        Handler of the Ti entry
        """
        val = self.Ti.get()
        val = round(min(1.0, max(0.0, val)), 2)
        self.Ti.set(val)
        self.slider_Ti.set(output_value=val, from_variable_callback=True)
        self.listener.changeOnTi(val)
        

    def commandEntryTj(self, event):
        """
        Handler of the Tj entry
        """
        val = self.Tj.get()
        val = round(min(1.0, max(0.0, val)), 2)
        self.Tj.set(val)
        self.slider_Tj.set(output_value=val, from_variable_callback=True)
        self.listener.changeOnTj(val)


    def commandEntryPf(self, event):
        """
        Handler of the Pf entry
        """
        val = self.Pf.get()
        val = round(min(100.0, max(1.0, val)), 2)
        self.Pf.set(val)
        self.slider_Pf.set(output_value=val, from_variable_callback=True)
        self.listener.changeOnPf()


    def commandSliderTi(self, newVal) -> None:
        """
        Handler of the Ti slider
        """
        val = round(newVal, 2)
        self.Ti.set(val)
        self.listener.changeOnTi(val)


    def commandSliderTj(self, newVal):
        """
        Handler of the Tj slider
        """
        val = round(newVal, 2)
        self.Tj.set(val)
        self.listener.changeOnTj(val)


    def commandSliderPf(self, newVal):
        """
        Handler of the Pf slider
        """
        val = round(newVal, 2)
        self.Pf.set(val)
        self.listener.changeOnPf()


    def setSliderTiValue(self, val:float):
        self.slider_Ti.set(output_value=val, from_variable_callback=True)


    def setSliderTjValue(self, val:float):
        self.slider_Tj.set(output_value=val, from_variable_callback=True)


    def onClickButtonObtainResults(self):
        if self.textButtonObtainResults.get() == "Obtain results":
            self.textButtonObtainResults.set("Reload results")
            self.listener.loadResultsVisualisation(self.master)
        self.listener.obtainResults()