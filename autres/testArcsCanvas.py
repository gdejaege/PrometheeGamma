import tkinter as tk

def P(x,y):
    """
    For convenience only.
    Transform point in cartesian (x,y) to Canvas (X,Y)
    As both system has difference y direction:
    Cartesian y-axis from bottom-left - up 
    Canvas Y-axis from top-left - down 
    """
    X = M + (x/xmax) * (W-2*M)
    Y = M + (1-(y/ymax)) * (H-2*M)
    return (X,Y)

def draw(window):
    """"
    Draw the lines
    """
    c = tk.Canvas(window, width=W, height=H)
    c.grid()
    
    # tuple of points to shape a 'bucket'
    points = P(60,0), P(90,50), P(50,100), P(10,50), P(40,0)
    
    fracture = c.create_line(points, arrow='last', fill='yellow')
    smooth = c.create_line(points, arrow='last', smooth=1)
   
"""
xmin is minimum value along cartesian x-axis
xmax is maximum value along cartesian x-axis
ymin is minimum value along cartesian y-axis
ymax is maximum value along cartesian y-axis
W is canvas width, in pixel
H is canvas height, in pixel
M is minimum margin inside canvas to ensure objects like arrow fully shown.

"""
M = 4  
W = 310
H = 210
xmin = 0
xmax = 100
ymin = 0
ymax = 100    

window = tk.Tk()
draw(window)
window.mainloop()