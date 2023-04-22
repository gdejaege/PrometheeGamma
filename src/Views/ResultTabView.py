from customtkinter import (CTkLabel, DoubleVar, CTkEntry, CTkSlider, StringVar, CTkButton)

class ResultTabView:
    def __init__(self, master) -> None:
        self.master = master
        
        # Parameters values
        self.Ti = DoubleVar(master=self.master, value=0.0)
        self.Tj = DoubleVar(master=self.master, value=0.0)
        self.Pf = DoubleVar(master=self.master, value=1.0)

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

        # Results visualisation screens
        #self.r_visualisation = ResultsVisualisation(master=self.master, method=self.method, fg_color="#ffffff")


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

        #self.r_visualisation.place(relx=0.02, y=150, relwidth=0.96, bordermode='inside')


    def commandEntryTi(self):
        pass


    def commandEntryTj(self):
        pass


    def commandEntryPf(self):
        pass


    def commandSliderTi(self):
        pass


    def commandSliderTj(self):
        pass


    def commandSliderPf(self):
        pass


    def onClickButtonObtainResults(self):
        pass