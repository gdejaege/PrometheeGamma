from customtkinter import CTkTextbox

class DisplayMatrixResultsView:
    def __init__(self, master) -> None:
        self.texbox_results = CTkTextbox(master=master, text_color="#000000", fg_color="#ffffff")


    def show(self, matrixResults:list):
        self.texbox_results.pack(expand=True, fill='both')
        self._print(matrixResults)


    def refresh(self, matrixResults:list):
        self._print(matrixResults)

    
    def _print(self, matrixResults:list):
        self.texbox_results.delete("1.0", "end")
        for i in range(len(matrixResults)):
            line = ""
            for e in matrixResults[i]:
                line += str(e) + ", "
            self.texbox_results.insert("end", line+"\n")