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


def grain_size(SN, Year, Month, File_List, Peak_Pos, Peak_Height, Peak_Id):    
    df_result = pd.DataFrame(columns=["File","FWHM","Grain Size","Peak"])   
    PATH = rf'\\10.138.112.112\Analysis Results\XRD\1_XRD\{Year}\{Month}\{SN}'
    try:
        os.mkdir(f'{PATH}\Result')
    except:
        pass
    result_PATH = rf'\\10.138.112.112\Analysis Results\XRD\1_XRD\{Year}\{Month}\{SN}\Result'
    for idx in range(len(File_List)):
               
        data = pd.read_csv(f'{PATH}\{File_List[idx]}', header=2, sep='\t')
        data.columns = ["Angle","Count"]
        Pos = np.array(Peak_Pos[idx]).astype(float)
        Height = np.array(Peak_Height[idx]).astype(float)
        Id = np.array(Peak_Id[idx]).astype(bool)
        initvars_C=[500,20,0,0]
        param_C_min=[10, 1, -inf, -inf]
        param_C_max=[inf, inf, inf,inf]

        for i in range(len(Pos)):
            initvars_C.append(Pos[i])
            initvars_C.append(Height[i])
            initvars_C.append(0.1)
            initvars_C.append(0.1)
            
            param_C_min.append(Pos[i]-2)
            param_C_min.append(0)
            param_C_min.append(0.01)
            param_C_min.append(0.01)
            
            param_C_max.append(Pos[i]+2)
            param_C_max.append(inf)
            param_C_max.append(5)
            param_C_max.append(5)

                
        Voigt = VoigtMaker(len(Pos))
        popt_V, pconv_V = curve_fit(Voigt,data["Angle"],data["Count"],p0=initvars_C,bounds=(param_C_min,param_C_max),maxfev=50000)
               
        pos_id = Pos[Id]
        height_id = Height[Id]        
        
        pl.plot(data["Angle"],Voigt(data["Angle"],*popt_V), linewidth = 0.4)
        pl.plot(data["Angle"],data["Count"], linewidth = 0.1)
        pl.plot(data["Angle"],popt_V[0]*exp(-data["Angle"]/popt_V[1]) + data["Angle"] * popt_V[2] +popt_V[3])    
        pl.plot(pos_id,height_id,"x")
        
        pl.savefig(f'{result_PATH}\{File_List[idx]}_Voigt.png')
        pl.clf()
        
        K=KforSherrer

        halfwidths=[]
        grains=[]

        peakbreaths=[]
        xs=[]
        ys=[]

        for peakidx in range(len(Id)):
            if Id[peakidx]:
                    
                halfwidth_sample=halfwidth_definer(data["Angle"],*popt_V[4+peakidx*4:8+peakidx*4])
                halfwidths.append(halfwidth_sample)

                grain_sample=  (K * wavelength) / (halfwidth_sample*np.pi/180 *np.cos (popt_V[4+peakidx*4]*np.pi/360))
                grains.append(grain_sample)

                xs.append(x_generator(halfwidth_sample*np.pi/180,popt_V[4+peakidx*4]*np.pi/360))
                ys.append(y_generator(halfwidth_sample*np.pi/180,popt_V[4+peakidx*4]*np.pi/360))
            
        K1=KforHW###############################################

        z = np.polyfit(xs,ys,1)
        
        pl.plot(xs,ys, "ro",color="red", markersize=5)
        xs.append(0)
        pl.plot(xs,z[0]*np.asarray(xs)+z[1], color="blue")
        pl.savefig(f'{result_PATH}\{File_List[idx]}_Halder_Wagner.png')
        pl.clf()
        
        result = {"File": File_List[idx], "FWHM" : halfwidths, "Grain Size" : grains, "Peak": Pos[Id].tolist()}
        
        df = pd.DataFrame(result)
        df_result = pd.concat([df_result,df])        
        
    return df_result