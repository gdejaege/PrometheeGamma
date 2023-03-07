from tkinter import *
#from tkinter import ttk
from tkinter import filedialog as fd
from customtkinter import (CTk, CTkEntry, CTkTabview, CTkTextbox, CTkLabel, CTkButton, CTkSlider, CTkToplevel, CTkFrame, CTkScrollbar, CTkCanvas, set_default_color_theme)
from PrometheeGamma import PrometheeGamma
from Criterion import Criterion
from OrthogonalGraph import OrthogonalGraph
from Schema import Schema
from Tabular import Tabular

class MyApp:
    """
    Main class of the Promethee Gamma app
    """
    def __init__(self, master=None) -> None:
        self.units = []
        """
        Matrix of units
        """
        self.criteria = []
        """
        List of criteria. The index correspond to the column number
        """
        self.f = []
        """
        List of preference function's types
        """
        self.p = []
        """
        List of preference parameters
        """
        self.q = []
        """
        List of indiferrence parameters
        """
        self.weights = []
        """
        List of criteria's weight
        """
        self.method = PrometheeGamma()
        """
        The used method
        """
        self.pf_types = {1:"Usual", 2:"U-shape", 3:"V-shape", 4:"Level", 5:"Linear", 6:"Gaussian"}
        
        # build ui
        self.ctk1 = CTk(master)
        self.ctk1.configure(cursor="arrow", height=500, width=800)
        set_default_color_theme("blue")
        self.ctk1.maxsize(2500, 2000)
        self.ctk1.minsize(600, 400)
        self.ctk1.resizable(True, True)
        self.ctk1.title("Promethee Gamma")
        
        self.tabview = CTkTabview(self.ctk1, fg_color="#ffffff")
        self.tabview.pack(expand=True, fill="both")


        ##########
        ## Data ##
        ##########

        self.tab1 = self.tabview.add("Data")
        self.tab1.configure(
            #background="#000000",
            #bg_color="#000080",
            border_color="#000080",
            corner_radius=5,
            cursor="arrow",
            fg_color="#ffffff")
        
        self.ctkb1 = CTkButton(self.tab1, text="Open a file", fg_color="#6cffff", text_color="#000000", corner_radius=5, command=self.open_file)
        self.ctkb1.pack(side="top", pady=10)
        #self.ctkb1.place(relx=0.1, rely=0.05)
        
        self.ctklabel_data_note = CTkLabel(self.tab1, text="Only csv files are accepted", fg_color="#ffffff", text_color="#000000", corner_radius=5)
        self.ctklabel_data_note.pack(side="top")
        #self.ctkb1.place(relx=0.1, rely=0.1)
        
        """
        # text_box
        self.ctktextbox1 = CTkTextbox(self.tab1)
        self.ctktextbox1.configure(fg_color="#dfdfdf", text_color="#000000")
        self.ctktextbox1.place(relx=0.05, rely=0.25, relheight=0.7, relwidth=0.9)
        """

        # tabular
        self.data_tab = Tabular(master=self.tab1, x=50, y=125)


        #############
        ## Results ##
        #############

        self.tab2 = self.tabview.add("Results")
        self.tab2.configure(
            #background="#000000",
            #bg_color="#000080",
            border_color="#000080",
            corner_radius=5,
            fg_color="#ffffff")

        label_Ti = CTkLabel(master=self.tab2, text="Global indifference threshold (Ti):", text_color="#000000", justify="left", padx=10, pady=10)
        label_Tj = CTkLabel(master=self.tab2, text="Global incomparability threshold (Tj):", text_color="#000000", justify="left", padx=10, pady=10)
        label_Pf = CTkLabel(master=self.tab2, text="Global preference factor (Pf):", text_color="#000000", justify="left", padx=10, pady=10)
        label_Ti.place(x=10, y=10)
        label_Tj.place(x=10, y=40)
        label_Pf.place(x=10, y=70)
        
        self.Ti = DoubleVar(master=self.tab2, value=0.0)
        self.Tj = DoubleVar(master=self.tab2, value=0.0)
        self.Pf = DoubleVar(master=self.tab2, value=1.0)
        self.entry_Ti = CTkEntry(master=self.tab2, textvariable=self.Ti, width=50)
        self.entry_Ti.bind("<Return>", command=self.command_entry_Ti)
        self.entry_Tj = CTkEntry(master=self.tab2, textvariable=self.Tj, width=50)
        self.entry_Tj.bind("<Return>", command=self.command_entry_Tj)
        self.entry_Pf = CTkEntry(master=self.tab2, textvariable=self.Pf, width=50)
        self.entry_Pf.bind("<Return>", command=self.command_entry_Pf)
        self.entry_Ti.place(x=250, y=10)
        self.entry_Tj.place(x=250, y=40)
        self.entry_Pf.place(x=250, y=70)
        
        self.slider_Ti= CTkSlider(master=self.tab2, from_=0, to=1, number_of_steps=100, command=self.command_slider_Ti)
        self.slider_Ti.set(output_value=self.Ti.get() ,from_variable_callback=True)
        self.slider_Ti.place(x=310, y=15)
        self.slider_Tj= CTkSlider(master=self.tab2, from_=0, to=1, number_of_steps=100, command=self.command_slider_Tj)
        self.slider_Tj.set(output_value=self.Tj.get() ,from_variable_callback=True)
        self.slider_Tj.place(x=310, y=45)
        self.slider_Pf= CTkSlider(master=self.tab2, from_=1, to=100, number_of_steps=1000, command=self.command_slider_Pf)
        self.slider_Pf.set(output_value=self.Pf.get() ,from_variable_callback=True)
        self.slider_Pf.place(x=310, y=75)

        self.text_b2 = StringVar(master=self.tab2, value="Obtain results")
        self.b2 = CTkButton(self.tab2, textvariable=self.text_b2, command=self.execute, fg_color="#6cffff", text_color="#000000")
        self.b2.place(relx=0.25, y=120, anchor="center")

        self.texbox_results = CTkTextbox(self.tab2, text_color="#000000", fg_color="#cfcfcf")

        self.b3 = CTkButton(self.tab2, text="See orthogonal graph", command=self.button_orthogonal_graph, fg_color="#6cffff", text_color="#000000")
        self.b3.place(relx=0.75, y=200, anchor="center")

        self.b4 = CTkButton(self.tab2, text="See graphical results", command=self.open_window_canvas, fg_color="#6cffff", text_color="#000000")
        self.b4.place(relx=0.75, y=250, anchor="center")

        # Main widget
        self.mainwindow = self.ctk1


    def run(self) -> None:
        """
        Launch the app loop
        """
        self.mainwindow.mainloop()


    def open_file(self) -> None:
        """
        Open and read a source file at csv format
        """
        # self.ctktextbox1.delete("1.0", "end")
        self.criteria.clear()
        self.weights.clear()
        self.q.clear()
        self.p.clear()
        self.f.clear()
        unames = []
        uval = []
        file = fd.askopenfile(mode="r", filetypes=(("csv file", "*.csv"), ("all files","*.*")))
        for line in file:
            line = line.strip()
            #self.ctktextbox1.insert("end", line+"\n")
            temp = line.split(',')
            if(temp[0] == 'c'):
                self.criteria = temp[1:]
            elif(temp[0] == 'w'):
                self.weights = temp[1:]
            elif(temp[0] == 'q'):
                self.q = temp[1:]
            elif(temp[0] == 'p'):
                self.p = temp[1:]
            elif(temp[0] == 'f'):
                self.f = temp[1:]
            else:
                unames.append(temp[0])
                uval.append(temp[1:])
                self.units.append(temp)
        file.close()

        self.data_tab.add_infos()
        self.data_tab.add_criteria(nb=len(self.criteria), names=self.criteria, weights=self.weights, types=self.f, pc=self.p, qc=self.q)
        self.data_tab.add_units(nb=len(unames), names=unames, values=uval)


    def get_data(self) -> None:
        """
        get the new data from the tabular in the tab Data
        """
        (self.criteria, self.weights, self.f, self.p, self.q, self.units) = self.data_tab.extracts_data()
        """
        print(self.criteria)
        print(self.weights)
        print(self.p)
        print(self.q)
        print(self.units)
        """


    def execute(self) -> None:
        """
        Execute the Promethee Gamma method
        """
        #if(self.text_b2.get() == "Reload results"):
        self.get_data()

        self.text_b2.set("Reload results")
        self.texbox_results.place(relx=0.05, rely=0.4, relheight=0.55, relwidth=0.43)

        self.method.clear()
        for i in range(len(self.criteria)):
            g = Criterion(self.criteria[i], float(self.weights[i]))
            ####
            print(self.f, self.p, self.q)
            ####
            g.set_pf(type=int(self.f[i]), pc=float(self.p[i]), qc=float(self.q[i]))
            for j in range(len(self.units)):
                g.add_unit(float(self.units[j][i+1]))
            self.method.add_criterion(g)
        
        for u in range(len(self.units)):
            self.method.add_unit(self.units[u][0])

        self.method.build_gamma_matrix()
        self.compute_results()


    def print_results(self) -> None:
        """
        Display the results in a textbox 
        """
        self.texbox_results.delete("1.0", "end")
        for i in range(len(self.units)):
            line = ""
            for e in self.method.get_matrix_results()[i]:
                line += str(e) + ", "
            self.texbox_results.insert("end", line+"\n")


    def compute_results(self) -> None:
        """
        Compute the results with the method
        """
        self.method.set_T_i(self.Ti.get())
        self.method.set_T_j(self.Tj.get())
        self.method.set_P_f(self.Pf.get())
        self.method.build_matrix_IPJ()
        self.method.final()
        self.print_results()
    

    def compute_change_Ti(self, val) -> None:
        """
        Recompute results after changing Ti
        """
        self.method.set_T_i(val)
        self.method.build_matrix_I()
        self.method.final()
        self.print_results()
    

    def command_entry_Ti(self, event) -> None:
        """
        Command funtion of entry_Ti
        """
        val = self.Ti.get()
        val = round(min(1.0, max(0.0, val)), 2)
        self.Ti.set(val)
        self.slider_Ti.set(output_value=val, from_variable_callback=True)
        self.compute_change_Ti(val)
        if(val > self.Tj.get()):
            self.changing_Tj_from_Ti(val)
    

    def command_slider_Ti(self, newval) -> None:
        """
        Command function of slider Ti
        """
        newval = round(newval, 2)
        self.Ti.set(newval)
        self.compute_change_Ti(newval)
        if(newval > self.Tj.get()):
            self.changing_Tj_from_Ti(newval)


    def compute_change_Tj(self, val) -> None:
        """
        Recompute results after changing Tj
        """
        self.method.set_T_j(val)
        self.method.build_matrix_J()
        self.method.final()
        self.print_results()
    

    def command_entry_Tj(self, event) -> None:
        """
        Command funtion of entry_Tj
        """
        val = self.Tj.get()
        val = round(min(1.0, max(0.0, val)), 2)
        self.Tj.set(val)
        self.slider_Tj.set(output_value=val ,from_variable_callback=True)
        self.compute_change_Tj(val)
        if(val < self.Ti.get()):
            self.changing_Ti_from_Tj(val)
    

    def command_slider_Tj(self, newval) -> None:
        """
        Command function of slider Tj
        """
        newval = round(newval, 2)
        self.Tj.set(newval)
        self.compute_change_Tj(newval)
        if(newval < self.Ti.get()):
            self.changing_Ti_from_Tj(newval)


    def changing_Tj_from_Ti(self, newval) -> None:
        self.Tj.set(newval)
        self.slider_Tj.set(output_value=newval ,from_variable_callback=True)
        self.compute_change_Tj(newval)


    def changing_Ti_from_Tj(self, newval) -> None:
        self.Ti.set(newval)
        self.slider_Ti.set(output_value=newval ,from_variable_callback=True)
        self.compute_change_Ti(newval)


    def compute_change_Pf(self, val) -> None:
        self.method.set_P_f(val)
        self.method.build_matrix_P()
        self.method.final()
        self.print_results()


    def command_entry_Pf(self, event) -> None:
        """
        Handler of the Pf entry
        """
        val = self.Pf.get()
        val = round(min(100.0, max(1.0, val)), 2)
        self.Pf.set(val)
        self.slider_Pf.set(output_value=val ,from_variable_callback=True)
        self.compute_change_Pf(val)
    

    def command_slider_Pf(self, newval) -> None:
        """
        Handler of the Pf slider
        """
        newval = round(newval, 2)
        self.Pf.set(newval)
        self.compute_change_Pf(newval)


    def button_orthogonal_graph(self) -> None:
        """
        Open a new window with to display the orthogonal graph of results
        """
        g = self.method.get_gamma_matrix()
        r = self.method.get_matrix_results()
        graph = OrthogonalGraph(g, r, Ti=self.Ti.get(), Tj=self.Tj.get())
        graph.show()


    def open_window_canvas(self) -> None:
        """
        Open a new window with a canvas space to display result in schematic form
        """
        size = len(self.units) * 80 + 100
        n=CTkToplevel(self.tab2)
        n.title('Graphical results')
        n.geometry("800x600")
        self.frame=CTkFrame(master=n, width=800, height=600)
        self.frame.pack(expand=True, fill=BOTH)
        c=CTkCanvas(self.frame,bg='#FFFFFF',width=750,height=550,scrollregion=(0,0,size,size))
        hbar=CTkScrollbar(master=self.frame,orientation=HORIZONTAL, command=c.xview)
        hbar.pack(side=BOTTOM,fill=X)
        vbar=CTkScrollbar(self.frame,orientation=VERTICAL, command=c.yview)
        vbar.pack(side=RIGHT,fill=Y)
        c.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        c.pack(side=LEFT,expand=True,fill=BOTH)
        self.frame.bind("<MouseWheel>", self._on_mousewheel)
        desssin = Schema(self.method.get_alternatives(), self.method.get_matrix_results(), c, size)
        desssin.build(self.method.get_scores())
        desssin.add_lines()
    

    def _on_mousewheel(self, event):
        self.frame.yview_scroll(-1*(event.delta/120), "units")