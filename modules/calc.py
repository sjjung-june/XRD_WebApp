import os
import glob
import numpy as np
import scipy.signal
import pylab as pl
from scipy.optimize import curve_fit
from numpy import exp, sign ,sin, pi, inf
import pandas as pd
from modules.utils import *

KforSherrer=0.94
KforHW=0.94
wavelength=1.54059


def grain_size(SN, FILE, Peak_Pos, Peak_Height):
    PATH = rf'\\10.138.112.112\Analysis Results\XRD\1_XRD\2022\05\{SN}'    
    FILE_PATH = f'{PATH}\{FILE}'
    data = pd.read_csv(FILE_PATH, header=2, sep='\t')
    data.columns = ["Angle","Count"]
    Peak_Pos = np.array(Peak_Pos).astype(float)
    Peak_Height = np.array(Peak_Height).astype(float)
    
    
    initvars_C=[500,20,0,0]
    param_C_min=[10, 1, -inf, -inf]
    param_C_max=[inf, inf, inf,inf]

    for i in range(len(Peak_Pos)):
        initvars_C.append(Peak_Pos[i])
        initvars_C.append(Peak_Height[i])
        initvars_C.append(0.1)
        initvars_C.append(0.1)
        
        param_C_min.append(Peak_Pos[i]-2)
        param_C_min.append(0)
        param_C_min.append(0.01)
        param_C_min.append(0.01)
        
        param_C_max.append(Peak_Pos[i]+2)
        param_C_max.append(inf)
        param_C_max.append(5)
        param_C_max.append(5)


    Voigt = VoigtMaker(len(Peak_Pos))
    popt_V, pconv_V = curve_fit(Voigt,data["Angle"],data["Count"],p0=initvars_C,bounds=(param_C_min,param_C_max),maxfev=50000)

    '''
    pl.plot(data["Angle"],Voigt(data["Angle"],*popt_V), linewidth = 0.4)
    pl.plot(data["Angle"],data["Count"], linewidth = 0.1)
    pl.plot(data["Angle"],popt_V[0]*exp(-data["Angle"]/popt_V[1]) + data["Angle"] * popt_V[2] +popt_V[3])
    pl.show()
    '''
    K=KforSherrer

    halfwidths=[]
    grains=[]

    peakbreaths=[]
    xs=[]
    ys=[]

    for peakidx in range(len(Peak_Pos)):
        halfwidth_sample=halfwidth_definer(data["Angle"],*popt_V[4+peakidx*4:8+peakidx*4])
        halfwidths.append(halfwidth_sample)

        grain_sample=  (K * wavelength) / (halfwidth_sample*np.pi/180 *np.cos (popt_V[4+peakidx*4]*np.pi/360))
        grains.append(grain_sample)

        xs.append(x_generator(halfwidth_sample*np.pi/180,popt_V[4+peakidx*4]*np.pi/360))
        ys.append(y_generator(halfwidth_sample*np.pi/180,popt_V[4+peakidx*4]*np.pi/360))
        
    K1=KforHW###############################################

    z = np.polyfit(xs,ys,1)
    '''
    pl.plot(xs,ys, "ro",color="red", markersize=5)
    xs.append(0)
    pl.plot(xs,z[0]*np.asarray(xs)+z[1], color="blue")
    pl.show()
    '''
    return {"Peak": Peak_Pos.tolist(), "FWHM" : halfwidths, "Grain Size" : grains}