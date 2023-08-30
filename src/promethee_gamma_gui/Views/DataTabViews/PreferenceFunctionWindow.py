from customtkinter import (CTkToplevel, CTkRadioButton, IntVar, StringVar)
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
import numpy as np


class PreferenceFunctionWindow:
    """
    A class to display the 6 types of preference function and allow to select one of them

    Attributes
    ----------
    root : CTkTopLevel
        the master frame
    typesDict : dict
        a dictionnary to link each type of preference function with a number (1 to 6)
    radioVar : IntVar
        a variable that contains the current preference function type
    textVar : StringVar
        a variable that contains the current preference function type name
    radioButtonList : list of CTkRadioButton
        a list that contains all radio buttons

    Methods
    -------
    """

    def __init__(self, master:CTkToplevel, textvar:StringVar, intvar:IntVar, typesDict:dict) -> None:
        """
        Parameters
        ----------
        master : CTkTopLevel
            the master frame
        textvar : StringVar
            a variable that contains the current preference function type name
        intvar : IntVar
            a variable that contains the current preference function type
        typesDict : dict
            a dictionnary to link each name of type of preference function with a number
        """
        self.root = master
        self.typesDict = typesDict
        self.radioVar = intvar
        self.textVar = textvar

        self.radioButtonList = []
        for i in self.typesDict.keys():
            text = "type " + str(i) + ": " + self.typesDict[i]
            r = CTkRadioButton(master=self.root, text=text, command=self.radiobutton_event, variable=self.radioVar, value=i)
            self.radioButtonList.append(r)


    def show(self):
        """show the window content
        """
        self.makeFig()

        r = 1
        c = 0
        for i in range(len(self.radioButtonList)):
            self.radioButtonList[i].grid(row=r, column=c)
            c += 1
            if i == 2:
                r = 3
                c = 0


    def makeFig(self):
        """Make the figures (draw the functions)
        """
        ################
        ### figure 1 ###
        ################

        fig1 = Figure(figsize=[14,4])

        # Plot usual function
        ax1 = fig1.add_subplot(1,3,1)
        ax1.set_title("Usual")
        (x, y) = self.usual()
        ax1.plot(x, y, 'b')
        ax1.axis([-0.2, 95, 0, 1.2])
        ax1.set_xticks([0])

        # Plot u-shape function
        ax2 = fig1.add_subplot(1,3,2)
        ax2.set_title("U-shape")
        (x, y) = self.u_shape()
        ax2.plot(x, y, 'b')
        ax2.text(49.5, -0.05, "q")
        ax2.axis([0, 95, 0, 1.2])
        ax2.set_xticks([0])

        # Plot vshape function
        ax3 = fig1.add_subplot(1,3,3)
        ax3.set_title("V-shape")
        (x, y) = self.v_shape()
        ax3.plot(x, y, 'b')
        ax3.plot([50,50], [0,1], 'b--', markersize=0.1)
        ax3.axis([0, 95, 0, 1.2])
        ax3.set_xticks([0])
        ax3.text(49.5, -0.05, "p")

        # Display fig1
        canvas1 = FigureCanvasTkAgg(fig1, master=self.root)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=0, columnspan=3)


        ################
        ### figure 2 ###
        ################

        fig2 = Figure(figsize=[14,4])

        # Plot level function
        ax4 = fig2.add_subplot(1,3,1)
        ax4.set_title("Level")
        (x, y) = self.level()
        ax4.plot(x, y, 'b')
        ax4.plot([63,63], [0,0.5], 'b--', markersize=0.1)
        ax4.axis([0, 95, 0, 1.2])
        ax4.set_xticks([0])
        ax4.text(33.5, -0.05, "q")
        ax4.text(62.5, -0.05, "p")

        # Plot linear function
        ax5 = fig2.add_subplot(1,3,2)
        ax5.set_title("Linear")
        (x, y) = self.linear()
        ax5.plot(x, y, 'b-')
        ax5.plot([65,65], [0,1], 'b--', markersize=0.1)
        ax5.axis([0, 95, 0, 1.2])
        ax5.set_xticks([0])
        ax5.text(34.5, -0.05, "q")
        ax5.text(64.5, -0.05, "p")

        # Plot gaussian function
        ax6 = fig2.add_subplot(1,3,3)
        ax6.set_title("Gaussian")
        (x, y) = self.gaussian()
        ax6.plot(x, y, 'b')
        ax6.set_xticks([0])
        ax6.axis([0, 3.9, 0, 1.2])

        # Display fig2
        canvas2 = FigureCanvasTkAgg(fig2, master=self.root)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=2, columnspan=3)


    def usual(self) -> tuple:
        """Computes points for usual function

        Returns
        -------
        tuple of 2 list of int
            the lists of abscissa and ordinates of usual function
        """
        x = np.arange(100)
        y = np.ones(100)
        x = x - 1
        x[0] = 0
        y[0] = 0
        return (x, y)
    

    def u_shape(self) -> tuple:
        """Computes points for u-shape function

        Returns
        -------
        tuple of 2 list of int
            the lists of abscissa and ordinates of u-shape function
        """
        x = np.arange(100)
        y = np.ones(100, dtype=int)
        x[50:] = x[50:] - 1
        x[50] = 50
        y[0:51] = 0
        return (x, y)
    

    def v_shape(self) -> tuple:
        """Computes points for v-shape function

        Returns
        -------
        tuple of 1 list of int and 1 list of float
            the lists of abscissa and ordinates of v-shape function
        """
        x = np.arange(100)
        y = np.arange(start=0, stop=2, step=0.02)
        y[50:] = 1
        return (x, y)
    

    def level(self) -> tuple:
        """Computes points for level function

        Returns
        -------
        tuple of 1 list of int and 1 list of float
            the lists of abscissa and ordinates of level function
        """
        x = np.arange(100)
        y = np.ones(100)
        x[35:] -= 1
        x[65:] -= 1
        y[:35] = 0
        y[35:65] = 0.5
        return (x, y)


    def linear(self) -> tuple:
        """Computes points for linear function

        Returns
        -------
        tuple of 1 list of int and 1 list of float
            the lists of abscissa and ordinates of linear function
        """
        x = np.arange(100)
        y = np.ones(100)
        y[:35] = 0
        y[35:65] = np.arange(start=0, stop=1, step=1/30)
        return (x, y)
    

    def gaussian(self) -> tuple:
        """Computes points for gaussian function

        Returns
        -------
        tuple of 2 list of float
            the lists of abscissa and ordinates of gaussian function
        """
        x = np.arange(start=0, stop=4, step=0.04)
        y = np.ones(100)
        for i in range(len(x)):
            y[i] = np.exp(-x[i]**2)
        y = -y + 1
        return (x, y)
    

    def radiobutton_event(self):
        """Handle radioButton events
        """
        self.textVar.set(self.typesDict[self.radioVar.get()])


    def get_radio_var(self):
        """Return the type of the selected preference function

        Returns
        -------
        int
            the value contained by radioVar
        """
        return self.radioVar.get()
