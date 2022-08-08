from math import  log10, pi, sqrt
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp2d

class Coil:
    """Coil Class with noise and signal considerations
    Arguments:
    n - number of turns 
    | dcoil - diameter of the coil (m) 
    | lcoil - length of coil (m) 
    | dwire - wire diameter (m) 
    | f - frequency in MHz 
    | SAMPLE properties 
    | alpha - sample diameter
    | beta - sample length 
    | Defaulted params: 
    | rho - Metal resistivity (ohm m) 
    | sigma -  sample Conductivity (S/m)
    |
    | i.e.
    | CuSolenoid = uSolenoid.Coil(8, .001, .002, .0004, 650, .0008, beta, rho=1.72e-8, sigma=1)

    | The Coil Class uses the following references:
    | part 1:
    | https://onlinelibrary.wiley.com/doi/abs/10.1002/1099-0534%282001%2913%3A2%3C128%3A%3AAID-CMR1002%3E3.0.CO%3B2-8
    | part 2:
    | https://onlinelibrary.wiley.com/doi/abs/10.1002/cmr.1008

    """
    def __init__(self, n, dcoil, lcoil, dwire, f, alpha, beta, rho=1.72e-8, sigma=1):
        self.n = n # number of turns
        self.dcoil = dcoil # diameter of coil
        self.lcoil = lcoil # length of coil
        self.dwire = dwire # wire diameter
        self.s = self.lcoil/self.n # spacing between wire
        self.u0 = 4*pi*1e-7 # H/m vacuum permeability 
        self.rho = rho # 1.72e-8 # (Cu) ohm meters
        self.ur = 1 # roughly for copper and siver
        self.f = f*1e6 # input is in MHz
        # sample stuff
        self.sigma = sigma # Siemans/m
        self.alpha = alpha # sample diameter
        self.beta = beta # sample length
    
    def Bxy(self):
        return self.n*self.u0 / (self.dcoil*sqrt(1+(self.lcoil/self.dcoil)**2))
    
    def Rcoil(self):
        # this changes with lcoil/dcoil
        # pick a value from the table for now
        # number of turns times the circumference...
        l = self.n*self.dcoil*pi
        rs = ((l/self.dwire)*sqrt(self.ur*self.u0*self.rho*self.f/pi))
        return rs*self.getEnhancementFactor()
          

    def Rleads(self):
        l = 4/1000 # length of the leads,
        d = self.dwire
        return (l/d) * sqrt(self.ur*self.u0*self.rho*self.f/pi) 

    def Rcap(self):
        #Q = 5.05*1e9*self.f**-2.35
        Q = 1000
        # calculate inductance
        # technically the leads also contribute inductance but i am ignoring it
        # correctors
        L = self.Lcoil()
        # need to estimate capacitance!
        Ctune = 1/(L*1e-9*(2*pi*self.f)**2)
        return 1/(self.f*2*pi*Q*Ctune)

    def Lcoil(self):
        J = 2.33*log10(self.dwire/self.s) + .515
        K_v = [.01,.07,.15,.18,.21,.24,.25,.27,.28,.29,.3]
        if (self.n > 11):
            K = .3
        else:
            K = K_v[self.n-1]
        L = (9850*self.dcoil*self.n**2 / (4.5 + 10*(self.lcoil/self.dcoil))) \
             - 628*self.dcoil*self.n*(J+K)
        return L
    
    def K(self):
        #J = 2.33*log10(self.dwire/self.s) + .515
        K_v = [.01,.07,.15,.18,.21,.24,.25,.27,.28,.29,.3]
        if (self.n > 11):
            K = .3
        else:
            K = K_v[self.n-1]
        return K

    def RsampleMagnetic(self):
        d = self.dcoil
        print(d)
        numerator = (pi*self.beta*self.sigma*(2*pi*self.f*self.u0*self.n*(self.alpha**2))**2)
        denom = (128*((d)**2 + (self.beta)**2))
        return (numerator/denom)

    def RsampleDielectric(self):
        
        w = 2*pi*self.f
        #w = 2*pi*750e6
        Lcoil = self.Lcoil()
        # eps
        enot = 8.85e-12 # F/m
        e0 = 78.32
        einf = 5.30
        tau = 8.27e-12
        epsPrime = einf + (e0 - einf)/(1+(w*tau)**2)
        epsDoublePrime = ((e0-einf)*w*tau)/(1+(w*tau)**2) + self.sigma/(w*enot)
        print('26.85 epsDoublePrime = {}'.format(epsDoublePrime))

        eps = epsPrime - 1j*epsDoublePrime

        fd = .94 # change to .25 in van heterens work

        H = .1126*self.lcoil/self.dcoil + .08 + (.27/((self.lcoil/self.dcoil)**.5))
        Cstray = 100*H*self.dcoil * 1e-12 # change to Farads
        print('Cstray = {}'.format(Cstray))
        Cprime = .5*Cstray
        C1 = Cprime*(1/(1-fd))
        print('C1 = {}'.format(C1))
        C2 = epsPrime*Cprime*(1/fd)
        print('C2 = {}'.format(C2))
        Rd = epsPrime/(w*C2*epsDoublePrime)
        Yreal = (Rd*(w*C1)**2)/(1+(((C1+C2)**2)*((w*Rd)**2)))
        Re = Yreal * Lcoil**2 * w**2

        return (((w*Lcoil)**2) * Yreal) 
        #return 60*self.RsampleMagnetic()

    def Rnmr(self):
        #return (self.Rcoil() + self.Rcap() + self.Rleads() + self.RsampleMagnetic())
        return (self.Rcoil() + self.RsampleDielectric() + self.Rcap() + self.Rleads() + self.RsampleMagnetic())
    
    def getEnhancementFactor(self):
        dos = self.dwire/(self.s)
        coil_ratio = self.lcoil/self.dcoil
        crs = [0.0,  0.2,  0.4,  0.6,  0.8,  1.0,  2.0,  4.0,  6.0,  8.0, 10.0, 1000000] # 12 the jth index
        dss = [.1,.2,.3,.4,.5,.6,.7,.8,.9,1]
        dss = [el for el in reversed(dss)]
        # ----------------------------------------
        # linear interpolate between the values
        ef_table = np.matrix('5.31, 5.45, 5.65, 5.80, 5.80, 5.55, 4.10, 3.54, 3.31, 3.20, 3.23, 3.41;\
            3.73, 3.84, 3.99, 4.11, 4.17, 4.10, 3.36, 3.05, 2.92, 2.90, 2.93, 3.11;\
                2.74, 2.83, 2.97, 3.10, 3.20, 3.17, 2.74, 2.60, 2.60, 2.62, 2.65, 2.81;\
                    2.12, 2.20, 2.28, 2.38, 2.44, 2.47, 2.32, 2.27, 2.29, 2.34, 2.37, 2.51;\
                        1.74, 1.77, 1.83, 1.89, 1.92, 1.94, 1.98, 2.01, 2.03, 2.08, 2.10, 2.22;\
                            1.44, 1.48, 1.54, 1.60, 1.64, 1.67, 1.74, 1.78, 1.80, 1.81, 1.83, 1.93;\
                                1.26, 1.29, 1.33, 1.38, 1.42, 1.45, 1.50, 1.54, 1.56, 1.57, 1.58, 1.65;\
                                    1.16, 1.19, 1.21, 1.22, 1.23, 1.24, 1.28, 1.32, 1.34, 1.34, 1.35, 1.40;\
                                        1.07, 1.08, 1.08, 1.10, 1.10, 1.10, 1.13, 1.15, 1.16, 1.16, 1.17, 1.19;\
                                            1.02, 1.02, 1.03, 1.03, 1.03, 1.03, 1.04, 1.04, 1.04, 1.04, 1.04, 1.05')
        # get the values and do a 2d linear interpolation:
        # ef(y,x) or crs,dss
        ef = interp2d(crs,dss,ef_table, kind='linear')
        e = ef(coil_ratio,dos)
        # correction, equation 11
        en = 1 + (e-1)*(1-1/self.n)
        return en

    def getSig(self):
        return (self.Bxy()*(2*pi*self.f)**2)/sqrt(self.Rnmr())
    
    