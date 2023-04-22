from customtkinter import (CTkFrame, CTkTabview, CTkTextbox, CTkCanvas, CTkScrollbar)
from tkinter import *
from Views.ResultTabViews.OrthogonalGraph import OrthogonalGraph
from Views.ResultTabViews.Schema import Schema

class ResultsVisualisation():
    class ViewListener:
        def getMethod(self):
            pass
    
    def __init__(self, master, **kwargs):
        self.frame = CTkTabview(master=master, fg_color="#ffffff")

        self.tab_tabular = self.frame.add("Tabular")
        self.tab_ograph = self.frame.add("Orthogonal graph")
        self.tab_rank = self.frame.add("Ranking")

        # Results textbox
        self.texbox_results = CTkTextbox(self.tab_tabular, text_color="#000000", fg_color="#ffffff")

        # Orthogonal graph
        self.o_graph = OrthogonalGraph(self.tab_ograph, [], [])

        # rank
        self.size_canvas = len(self.method.get_alternatives()) * 80 + 100
        self.canvas=CTkCanvas(self.tab_rank, bg='#FFFFFF',width=750,height=550,scrollregion=(0,0,self.size_canvas,self.size_canvas))
        self.hbar=CTkScrollbar(master=self.tab_rank,orientation=HORIZONTAL, command=self.canvas.xview)
        self.vbar=CTkScrollbar(self.tab_rank, orientation=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.tab_rank.bind("<MouseWheel>", self._on_mousewheel)
        self.desssin = Schema([], [], self.canvas, self.size_canvas)


    def show(self):
        # main
        self.frame.place(relx=0.02, y=150, relwidth=0.96, bordermode='inside')
        
        # textbox
        self.texbox_results.pack(expand=True, fill='both')
        
        # Orthogonal graph
        self.o_graph.show()

        # rank
        self.hbar.pack(side=BOTTOM,fill=X)
        self.vbar.pack(side=RIGHT,fill=Y)
        self.canvas.pack(side=LEFT,expand=True,fill=BOTH)
        self.desssin.show()



    def update(self):
        self.print_results()
        self.draw_ograph()
        self.draw_canvas()


    def print_results(self) -> None:
        """
        Display the results in a textbox 
        """
        self.texbox_results.delete("1.0", "end")
        for i in range(len(self.method.get_alternatives())):
            line = ""
            for e in self.method.get_matrix_results()[i]:
                line += str(e) + ", "
            self.texbox_results.insert("end", line+"\n")

    
    def draw_ograph(self) -> None:
        self.o_graph.set_gamma_matrix_and_results(gamma_matrix=self.method.get_gamma_matrix(), matrix_results=self.method.get_matrix_results())
        self.o_graph.show_graph()

    
    def draw_canvas(self) -> None:
        """
        Display result in a schematic ranking
        """
        self.canvas.delete('all')
        self.size_canvas = len(self.method.get_alternatives()) * 80 + 100
        self.canvas.configure(width=750,height=550,scrollregion=(0,0,self.size_canvas,self.size_canvas))
        self.desssin = Schema(self.method.get_alternatives(), self.method.get_matrix_results(), self.canvas, self.tab_rank.winfo_screenwidth())
        self.desssin.build(self.method.get_scores())
        self.desssin.add_lines()
    

    def _on_mousewheel(self, event):
        self.tab_rank.yview_scroll(-1*(event.delta/120), "units")