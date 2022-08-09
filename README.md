# Solenoid-Designer
## Purpose:
### Gives the RF engineer complete control over every microsolenoid parameter, from temperature to sizing, in order to achieve the ideal microsolenoid for an MR microscopy experiment
### most of the content is worth based on these two manuscripts by Minard and Wind
### [Solenoidal microcoil design. Part I: Optimizing RF homogeneity and coil dimensions](https://doi.org/10.1002/1099-0534(2001)13:2<128::AID-CMR1002>3.0.CO;2-8) 
### [Solenoidal microcoil design—Part II: Optimizing winding parameters for maximum signal-to-noise performance](https://doi.org/10.1002/cmr.1008)
## Contents:
### Coil Class with noise and signal considerations
    Arguments:
    | n - number of turns 
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

### Balun Designer:
    Simple Floating Coffee can balun designer based on the self-resonance of two concentric cylinders surrounding a coaxial cable.


## To do:
    Add UI to change variables
    Add Hoult's solenoid considerations