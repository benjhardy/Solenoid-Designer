import tkinter as tk
import uSolenoid as us
# Benjamin Hardy, 8-09-2022
# Solenoid designer GUI
# Visualize Solenoid design parameters
#
# most of this is from: https://realpython.com/python-gui-tkinter/
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
# now create a button that takes all the values and spits out a plot inside the window

button = tk.Button(
    text="Graph Stuff",
    width=10,
    height=2,
    bg="blue",
    fg="yellow"
)
button.pack()
window.mainloop()