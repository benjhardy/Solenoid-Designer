# Benjamin Hardy, 8-09-2022
# Solenoid designer GUI
# Visualize Solenoid design parameters
#
# most of this is from: https://realpython.com/python-gui-tkinter/
# embedded plots: https://www.geeksforgeeks.org/how-to-embed-matplotlib-charts-in-tkinter-gui/#:~:text=Embedding%20the%20Plot%3A,a%20toolbar%20at%20the%20bottom.
# tk.pack() options : https://www.tutorialspoint.com/python/tk_pack.htm
# Imports:
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import uSolenoid as us
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
#plt.rcParams['text.usetex'] = True


def runRhoCoil(n,dcoil,lcoil,dwire,freq,alpha,beta,rho,sigma):
    # change rho
    dwire = np.linspace(1e-6,100e-6,50)
    #n = 6
    #freq = 650
    #dcoil = 1.5/1000
    #alpha = dcoil
    
    #lcoil = 6/1000
    #beta = lcoil
    #dwire = 0.4/1000
    ##
    rcoil_v = np.array([]) 
    snr_v = np.array([]) 
    for d in dwire:
        c = us.Coil(n,dcoil,lcoil,d,freq,rho,alpha,beta,sigma)
        rcoil_v = np.append(rcoil_v,c.Rcoil())
        snr_v = np.append(snr_v,c.getSig())

    return dwire, rcoil_v, snr_v



def plot(N,dcoil,lcoil,dwire,freqs,alpha,beta,rho,sigma):
    # the figure that will contain the plot
    fig = plt.figure(figsize = (3, 3),
                 dpi = 100)
    
    # update the class so that it handles vectors!
    #for f in freqs:
    #    s = us.Coil(int(N.get()), float(dcoil.get()), float(lcoil.get()), float(dwire.get()), f, float(alpha.get()), float(beta.get()), float(rho.get()), float(sigma.get()))
    #    sig.append(s.getSig())
    dwire, rcoil_v, snr_v = runRhoCoil(int(N.get()), float(dcoil.get()), float(lcoil.get()), float(dwire.get()), float(f.get()), float(alpha.get()), float(beta.get()), float(rho.get()), float(sigma.get()))
    # adding the subplot
    plot1 = fig.add_subplot(111)
    fig.suptitle('SNR vs Wire Diameter N = 8',fontsize=15, fontweight='bold')
    plot1.set_xlabel(r'wire diameter $(µm)$',fontsize=15, fontweight='bold')
    plot1.set_ylabel(r'$SNR$',fontsize=20, fontweight='bold')
    
    # plotting the graph
    plot1.plot(dwire*1e6,snr_v)
    #fig.set(xlabel=r'$wire diameter (\mum)$', ylabel=r'$SNR$',fontsize=30, fontweight='bold')
    #ax.xlabel(r'$wire diameter (\mum)$',fontsize=30, fontweight='bold')
    #fig.ylabel(r'$R_{coil}(\Omega)$',fontsize=30, fontweight='bold')
    #plot1.ylabel(r'$SNR$',fontsize=30, fontweight='bold')
    #plot1.yticks(fontsize=20)
    #fig.xticks(fontsize=20)
    
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,master = window)  
    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack(padx=10)
  
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,window)
    toolbar.update()
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


window = tk.Tk()
window.title('Solenoid Designer')
#window.geometry()
greeting = tk.Label(text="Solenoid Designer")
greeting.pack()
# CuSolenoid = uSolenoid.Coil(8, .001, .002, .0004, 650, .0008, beta, rho=1.72e-8, sigma=1)
l = tk.Label(text="Number of Turns (N):")
N = tk.Entry()
l.pack()
N.insert(0,8)
N.pack()
l = tk.Label(text="dcoil - diameter of the coil (m):")
dcoil = tk.Entry()
l.pack()
dcoil.insert(0,.001)
dcoil.pack()
l = tk.Label(text="lcoil - length of coil (m)")
lcoil = tk.Entry()
l.pack()
lcoil.insert(0,.003)
lcoil.pack()
l = tk.Label(text="dwire - wire diameter (m)")
dwire = tk.Entry()
l.pack()
dwire.insert(0,.0001)
dwire.pack()
l = tk.Label(text="f - frequency in MHz")
f = tk.Entry()
l.pack()
f.insert(0,650)
f.pack()
l = tk.Label(text="alpha - sample diameter")
alpha = tk.Entry()
l.pack()
alpha.insert(0,.001)
alpha.pack()
l = tk.Label(text="beta - sample length")
beta = tk.Entry()
l.pack()
beta.insert(0,.003)
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
button.pack(padx=10)
window.mainloop()

# buttons