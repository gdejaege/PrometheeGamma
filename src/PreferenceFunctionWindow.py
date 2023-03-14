from customtkinter import (CTkToplevel, CTkRadioButton, IntVar, StringVar)
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
import numpy as np

class PreferenceFunctionWindow:

    def __init__(self, master:CTkToplevel, textvar:StringVar, intvar:IntVar) -> None:
        self.root = master
        self.dico_types = {1:"Usual", 2:"U-shape", 3:"V-shape", 4:"Level", 5:"Linear", 6:"Gaussian"}

        ################
        ### figure 1 ###
        ################

        self.fig1 = Figure(figsize=[14,4])

        ax1 = self.fig1.add_subplot(1,3,1)
        ax1.set_title("Usual")
        (x, y) = self.usual()
        ax1.plot(x, y, 'b')
        ax1.axis([-0.2, 95, 0, 1.2])
        ax1.set_xticks([0])

        ax2 = self.fig1.add_subplot(1,3,2)
        ax2.set_title("U-shape")
        (x, y) = self.u_shape()
        ax2.plot(x, y, 'b')
        ax2.text(49.5, -0.05, "q")
        ax2.axis([0, 95, 0, 1.2])
        ax2.set_xticks([0])

        ax3 = self.fig1.add_subplot(1,3,3)
        ax3.set_title("V-shape")
        (x, y) = self.v_shape()
        ax3.plot(x, y, 'b')
        ax3.plot([50,50], [0,1], 'b--', markersize=0.1)
        ax3.axis([0, 95, 0, 1.2])
        ax3.set_xticks([0])
        ax3.text(49.5, -0.05, "p")

        canvas1 = FigureCanvasTkAgg(self.fig1, master=self.root)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=0, columnspan=3)


        ################
        ### figure 2 ###
        ################

        self.fig2 = Figure(figsize=[14,4])

        ax4 = self.fig2.add_subplot(1,3,1)
        ax4.set_title("Level")
        (x, y) = self.level()
        ax4.plot(x, y, 'b')
        ax4.plot([63,63], [0,0.5], 'b--', markersize=0.1)
        ax4.axis([0, 95, 0, 1.2])
        ax4.set_xticks([0])
        ax4.text(33.5, -0.05, "q")
        ax4.text(62.5, -0.05, "p")

        ax5 = self.fig2.add_subplot(1,3,2)
        ax5.set_title("Linear")
        (x, y) = self.linear()
        ax5.plot(x, y, 'b-')
        ax5.plot([65,65], [0,1], 'b--', markersize=0.1)
        ax5.axis([0, 95, 0, 1.2])
        ax5.set_xticks([0])
        ax5.text(34.5, -0.05, "q")
        ax5.text(64.5, -0.05, "p")

        ax6 = self.fig2.add_subplot(1,3,3)
        ax6.set_title("Gaussian")
        (x, y) = self.gaussian()
        ax6.plot(x, y, 'b')
        ax6.set_xticks([0])
        ax6.axis([0, 3.9, 0, 1.2])

        canvas2 = FigureCanvasTkAgg(self.fig2, master=self.root)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=2, columnspan=3)


        #####################
        ### Radio buttons ###
        #####################

        self.radio_var = intvar
        self.textvar = textvar

        radiobutton_1 = CTkRadioButton(master=self.root, text="type 1: Usual", command=self.radiobutton_event, variable= self.radio_var, value=1)
        radiobutton_2 = CTkRadioButton(master=self.root, text="type 2: U-shape", command=self.radiobutton_event, variable= self.radio_var, value=2)
        radiobutton_3 = CTkRadioButton(master=self.root, text="type 3: V-shape", command=self.radiobutton_event, variable= self.radio_var, value=3)

        radiobutton_4 = CTkRadioButton(master=self.root, text="type 4: Level", command=self.radiobutton_event, variable= self.radio_var, value=4)
        radiobutton_5 = CTkRadioButton(master=self.root, text="type 2: Linear", command=self.radiobutton_event, variable= self.radio_var, value=5)
        radiobutton_6 = CTkRadioButton(master=self.root, text="type 3: Gaussian", command=self.radiobutton_event, variable= self.radio_var, value=6)

        radiobutton_1.grid(row=1, column=0)
        radiobutton_2.grid(row=1, column=1)
        radiobutton_3.grid(row=1, column=2)

        radiobutton_4.grid(row=3, column=0)
        radiobutton_5.grid(row=3, column=1)
        radiobutton_6.grid(row=3, column=2)


    def usual(self) -> tuple:
        x = np.arange(100)
        y = np.ones(100)
        x = x - 1
        x[0] = 0
        y[0] = 0
        return (x, y)
    

    def u_shape(self) -> tuple:
        x = np.arange(100)
        y = np.ones(100, dtype=int)
        x[50:] = x[50:] - 1
        x[50] = 50
        y[0:51] = 0
        return (x, y)
    

    def v_shape(self) -> tuple:
        x = np.arange(100)
        y = np.arange(start=0, stop=2, step=0.02)
        y[50:] = 1
        return (x, y)
    

    def level(self) -> tuple:
        x = np.arange(100)
        y = np.ones(100)
        x[35:] -= 1
        x[65:] -= 1
        y[:35] = 0
        y[35:65] = 0.5
        return (x, y)


    def linear(self) -> tuple:
        x = np.arange(100)
        y = np.ones(100)
        y[:35] = 0
        y[35:65] = np.arange(start=0, stop=1, step=1/30)
        return (x, y)
    

    def gaussian(self) -> tuple:
        x = np.arange(start=0, stop=4, step=0.04)
        y = np.ones(100)
        for i in range(len(x)):
            y[i] = np.exp(-x[i]**2)
        y = -y + 1
        return (x, y)
    

    def radiobutton_event(self):
        self.textvar.set(self.dico_types[self.radio_var.get()])
        #print("radiobutton toggled, current value:", self.radio_var.get())


    def get_radio_var(self):
        return self.radio_var.get()
