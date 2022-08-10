# Benjamin Hardy, 8-09-2022
# Solenoid designer GUI
# Visualize Solenoid design parameters
#
# most of this is from: https://realpython.com/python-gui-tkinter/
# embedded plots: https://www.geeksforgeeks.org/how-to-embed-matplotlib-charts-in-tkinter-gui/#:~:text=Embedding%20the%20Plot%3A,a%20toolbar%20at%20the%20bottom.
# tk.pack() options : https://www.tutorialspoint.com/python/tk_pack.htm
# Imports:
import tkinter as tk
from matplotlib.figure import Figure
import numpy as np
import uSolenoid as us
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)


def plot(N,dcoil,lcoil,dwire,freqs,alpha,beta,rho,sigma):
    # the figure that will contain the plot
    fig = Figure(figsize = (5, 5),
                 dpi = 100)
    sig = []
    # update the class so that it handles vectors!
    for f in freqs:
        s = us.Coil(int(N.get()), float(dcoil.get()), float(lcoil.get()), float(dwire.get()), f, float(alpha.get()), float(beta.get()), float(rho.get()), float(sigma.get()))
        sig.append(s.getSig())
    
    # adding the subplot
    plot1 = fig.add_subplot(111)
    # plotting the graph
    plot1.plot(freqs,sig)
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,master = window)  
    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
  
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,window)
    toolbar.update()
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()


window = tk.Tk()
window.title('Solenoid Designer')
greeting = tk.Label(text="Solenoid Designer")
greeting.pack()
# CuSolenoid = uSolenoid.Coil(8, .001, .002, .0004, 650, .0008, beta, rho=1.72e-8, sigma=1)
l = tk.Label(text="Number of Turns (N):")
N = tk.Entry()
l.pack()
N.pack()
l = tk.Label(text="dcoil - diameter of the coil (m):")
dcoil = tk.Entry()
l.pack()
dcoil.pack()
l = tk.Label(text="lcoil - length of coil (m)")
lcoil = tk.Entry()
l.pack()
lcoil.pack()
l = tk.Label(text="dwire - wire diameter (m)")
dwire = tk.Entry()
l.pack()
dwire.pack()
l = tk.Label(text="f - frequency in MHz")
f = tk.Entry()
l.pack()
f.pack()
l = tk.Label(text="alpha - sample diameter")
alpha = tk.Entry()
l.pack()
alpha.pack()
l = tk.Label(text="beta - sample length")
beta = tk.Entry()
l.pack()
beta.pack()
l = tk.Label(text="rho - Metal resistivity (ohm m)")
rho = tk.Entry()
l.pack()
rho.insert(0,1.72e-8)
rho.pack()
l = tk.Label(text="sigma -  sample Conductivity (S/m)")
sigma = tk.Entry()
l.pack()
sigma.insert(0,1)
sigma.pack()
# test array
freqs = np.arange(300,950,100)
button = tk.Button(
    master = window,
    command = lambda: plot(N,dcoil,lcoil,dwire,freqs,alpha,beta,rho,sigma),
    text="Graph Stuff",
    width=10,
    height=2,
    bg="blue",
    fg="yellow"
)
button.pack()
window.mainloop()