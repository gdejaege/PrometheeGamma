# Import the required libraries
from tkinter import *
import tkinter.messagebox

# Create an instance of Tkinter Frame
win = Tk()

# Set the geometry of Tkinter Frame
win.geometry("700x350")

def open_win():
   #out = tkinter.messagebox.showwarning(title="attention", message="ceci est un attention")
   out = tkinter.messagebox.showerror(title="erreur", message="ceci est une erreur")
   print(out)
   #out = tkinter.messagebox.askquestion('Prompt', 'Do you want to Continue?')
   #if out == 'yes':
      #Label(win, text="Thank You for your Response!", font=('Helvetica 22 bold')).pack(pady=40)
   #else:
    #  win.destroy()

# Create a Button
button = Button(win, text="Click Me", command=open_win, font=('Helvetica 14 bold'), foreground='OrangeRed3',background="white")
button.pack(pady=50)
win.mainloop()