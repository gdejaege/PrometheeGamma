from sys import maxsize
from customtkinter import (CTkLabel, DoubleVar, CTkEntry, CTkSlider, StringVar, CTkButton, CTkFrame)
from Resources.ScrollableFrame import ScrollableFrame

INFINITY = maxsize

class ResultTabView:
    """
    A class to display the result tab view of the PROMETHEE Gamma GUI application

    Attributes
    ----------
    root : CTkFrame
        the parent master frame
    scrollableFrame : ScrollableFrame
        the scrollableFrame
    master : CTkFrame
        the master frame
    listener : ResultTabView.ViewListener
        the view listener
    Ti : DoubleVar
        the indifference threshold of PROMETHEE Gamma method
    Tj : DoubleVar
        the incompatibility threshold of PROMETHEE Gamma method
    Pf : DoubleVar
        the preference parameter of PROMETHEE Gamma method
    TiLabel : CTkLabel
        the label to see the Ti value
    TjLabel : CTkLabel
        the label to see the Tj value
    PfLabel : CTkLabel
        the label to see the Pf value
    TiEntry : CTkEntry
        the entry to set the Ti value
    TjEntry : CTkEntry
        the entry to set the Tj value
    PfEntry : CTkEntry
        the entry to set the Pf value
    TiSlider : CTkSlider
        the slider to set the Ti value
    TjSlider : CTkSlider
        the slider to set the Tj value
    PfSlider : CTkSlider
        the slider to set the Pf value
    textObtainResultsButton : StringVar
        a StringVar that contain the text of the obtainResultsButton
    ObtainResultsButton : CTkButton
        a button to obtain/relaod results of PROMETHEE Gamma method

    Methods
    -------
    setListener(l:ViewListener)
        set the listener
    show()
        show the view
    refresh()
        refresh the values of PROMETHEE Gamma method parameters
    commandTiEntry(event)
        handle TiEntry events
    commandTjEntry(event)
        handle TjEntry events
    commandPfEntry(event)
        handle PfEntry events
    commandTiSlider(event)
        handle TiSlider events
    commandTjSlider(event)
        handle TjSlider events
    commandPfSlider(event)
        handle PfSlider events
    setTiSliderValue(val:float)
        set the value of TiSlider
    setTjSliderValue(val:float)
        set the value of TjSlider
    onClickObtainResultsButton()
        handle clicks on obtainResultsButton
    """

    class ViewListener:
        """
        An interrface for the listener

        Methods
        -------
        changeOnTi(newValue:float)
            handle change on Ti value
        changeOnTj(newValue:float)
            handle change on Tj value
        changeOnPf()
            handle change on Pf value
        obtainResults()
            load results of PROMETHEE Gamma method
        """

        def changeOnTi(self, newValue:float):
            pass
        def changeOnTj(self, newValue:float):
            pass
        def changeOnPf(self):
            pass
        def obtainResults(self, load):
            pass
    
    
    def __init__(self, master, Ti:DoubleVar, Tj:DoubleVar, Pf:DoubleVar) -> None:
        """
        Parameters
        ----------
        master : CTkFrame
            the master frame
        Ti : DoubleVar
            the indifference threshold of PROMETHEE Gamma method
        Tj : DoubleVar
            the incompatibility threshold of PROMETHEE Gamma method
        Pf : DoubleVar
            the preference parameter of PROMETHEE Gamma method
        """
        # Initialize the frame
        self.master = master
        self.listener = None
        
        # Parameters values
        self.Ti = Ti
        self.Tj = Tj
        self.Pf = Pf

        # Line frames (for pack)
        self.l0 = CTkFrame(master=self.master, bg_color="#ffffff", fg_color="#ffffff")
        self.l1 = CTkFrame(master=self.master, bg_color="#ffffff", fg_color="#ffffff")
        self.l2 = CTkFrame(master=self.master, bg_color="#ffffff", fg_color="#ffffff")

        # Labels
        self.TiLabel = CTkLabel(master=self.l0, text="Global indifference threshold (Ti):", text_color="#000000", justify="left", width=350, padx=10, pady=10)
        self.TjLabel = CTkLabel(master=self.l1, text="Global incomparability threshold (Tj):", text_color="#000000", justify="left", width=350, padx=10, pady=10)
        self.PfLabel = CTkLabel(master=self.l2, text="Global preference factor (Pf):", text_color="#000000", justify="left", width=350, padx=10, pady=10)
        
        #Entries
        self.TiEntry = CTkEntry(master=self.l0, textvariable=self.Ti, width=200)
        self.TiEntry.bind("<Return>", command=self.commandTiEntry)
        self.TjEntry = CTkEntry(master=self.l1, textvariable=self.Tj, width=200)
        self.TjEntry.bind("<Return>", command=self.commandTjEntry)
        self.PfEntry = CTkEntry(master=self.l2, textvariable=self.Pf, width=200)
        self.PfEntry.bind("<Return>", command=self.commandPfEntry)
        
        # Sliders
        self.TiSlider = CTkSlider(master=self.l0, from_=0, to=1, number_of_steps=100, command=self.commandTiSlider)
        self.TiSlider.set(output_value=self.Ti.get() ,from_variable_callback=True)
        self.TjSlider = CTkSlider(master=self.l1, from_=0, to=1, number_of_steps=100, command=self.commandTjSlider)
        self.TjSlider.set(output_value=self.Tj.get() ,from_variable_callback=True)
        self.PfSlider = CTkSlider(master=self.l2, from_=1, to=100.01, number_of_steps=991, command=self.commandPfSlider)
        self.PfSlider.set(output_value=self.Pf.get() ,from_variable_callback=True)

        # Button
        self.textObtainResultsButton = StringVar(master=self.master, value="Obtain results")
        self.ObtainResultsButton = CTkButton(self.master, textvariable=self.textObtainResultsButton, command=self.onClickObtainResultsButton, fg_color="#6cffff", text_color="#000000")

        # Result visualisation frame
        self.rVis = CTkFrame(master=self.master, bg_color="#ffffff", fg_color="#ffffff")


    def setListener(self, l:ViewListener) -> None:
        """Set the listener

        Parameters
        ----------
        l : ViewListener
            the new listener
        """
        self.listener = l


    def show(self) -> None:
        """Show the view
        """

        self.l0.pack(fill="x")
        self.l1.pack(fill="x")
        self.l2.pack(fill="x")

        self.TiLabel.pack(side="left", anchor="nw", padx=5,pady=2)
        self.TjLabel.pack(side="left", anchor="nw", padx=5,pady=2)
        self.PfLabel.pack(side="left", anchor="nw", padx=5,pady=2)
        
        self.TiEntry.pack(side="left", anchor="nw", padx=5,pady=2)
        self.TjEntry.pack(side="left", anchor="nw", padx=5,pady=2)
        self.PfEntry.pack(side="left", anchor="nw", padx=5,pady=2)

        self.TiSlider.pack(side="left", anchor="w", padx=5,pady=2)
        self.TjSlider.pack(side="left", anchor="w", padx=5,pady=2)
        self.PfSlider.pack(side="left", anchor="w", padx=5,pady=2)

        self.ObtainResultsButton.pack(pady=10)

        self.rVis.pack(expand=True, fill="both")


    def refresh(self):
        """Refresh the values of PROMETHEE Gamma method parameters
        """
        self.commandTiEntry(0)
        self.commandTjEntry(0)
        self.commandPfEntry(0)


    def commandTiEntry(self, event) -> None:
        """Handle TiEntry events

        Parameters
        ----------
        event : Event
            an entry event
        """
        val = self.Ti.get()
        val = round(min(1.0, max(0.0, val)), 2)
        self.Ti.set(val)
        self.TiSlider.set(output_value=val, from_variable_callback=True)
        self.listener.changeOnTi(val)
        

    def commandTjEntry(self, event):
        """Handle TjEntry events

        Parameters
        ----------
        event : Event
            an entry event
        """
        val = self.Tj.get()
        val = round(min(1.0, max(0.0, val)), 2)
        self.Tj.set(val)
        self.TjSlider.set(output_value=val, from_variable_callback=True)
        self.listener.changeOnTj(val)


    def commandPfEntry(self, event):
        """Handle PfEntry events

        Parameters
        ----------
        event : Event
            an entry event
        """
        val = self.Pf.get()
        val = round(min(INFINITY,max(1.0, val)), 2)
        self.Pf.set(val)
        if val > 100:
            val = 100.01
        self.PfSlider.set(output_value=val, from_variable_callback=True)
        self.listener.changeOnPf()


    def commandTiSlider(self, newVal) -> None:
        """Handle TiSlider events

        Parameters
        ----------
        event : Event
            a slider event
        """
        val = round(newVal, 2)
        self.Ti.set(val)
        self.listener.changeOnTi(val)


    def commandTjSlider(self, newVal):
        """Handle TjSlider events

        Parameters
        ----------
        event : Event
            a slider event
        """
        val = round(newVal, 2)
        self.Tj.set(val)
        self.listener.changeOnTj(val)


    def commandPfSlider(self, newVal):
        """Handle PfSlider events

        Parameters
        ----------
        event : Event
            a slider event
        """
        val = max(1.0,round(newVal, 2))
        if val > 100:
            val = INFINITY
        self.Pf.set(val)
        self.listener.changeOnPf()


    def setTiSliderValue(self, val:float):
        """Set the value of TiSlider

        Parameters
        ----------
        val : float
            the new value for TiSlider
        """
        self.TiSlider.set(output_value=val, from_variable_callback=True)


    def setTjSliderValue(self, val:float):
        """Set the value of TjSlider

        Parameters
        ----------
        val : float
            the new value for TjSlider
        """
        self.TjSlider.set(output_value=val, from_variable_callback=True)


    def updateParameters(self):
        val = self.Ti.get()
        val = round(min(1.0, max(0.0, val)), 2)
        self.Ti.set(val)
        self.TiSlider.set(output_value=val, from_variable_callback=True)
        
        val = self.Tj.get()
        val = round(min(1.0, max(0.0, val)), 2)
        self.Tj.set(val)
        self.TjSlider.set(output_value=val, from_variable_callback=True)
        
        val = self.Pf.get()
        val = round(min(INFINITY,max(1.0, val)), 2)
        self.Pf.set(val)
        if val > 100:
            val = 100.01
        self.PfSlider.set(output_value=val, from_variable_callback=True)


    def onClickObtainResultsButton(self):
        """Handle clicks on obtainResultsButton
        """
        txt = self.textObtainResultsButton.get()
        self.listener.obtainResults(txt == "Obtain results")


    def ObtainResultsChange(self):
        self.textObtainResultsButton.set("Reload results")

    
    def reset(self):
        self.textObtainResultsButton.set("Obtain results")

    
    def getMaster(self):
        return self.rVis