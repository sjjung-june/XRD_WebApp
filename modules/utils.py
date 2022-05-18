import numpy as np
from scipy.special import wofz
from numpy import exp, sign ,sin, pi, inf

def halfwidth_definer (X, cen1, ampV1, sigmaV1, gammaV1):
    half_height=ampV1*Single_Voigt(0,sigmaV1, gammaV1)/2
    functional_peak = ampV1*  Single_Voigt(X-cen1,sigmaV1, gammaV1)
    intersection1 = np.argwhere(np.diff(np.sign(functional_peak-half_height))<0).reshape(-1) +0
    intersection2 = np.argwhere(np.diff(np.sign(functional_peak-half_height))>0).reshape(-1) +0
    return (X[intersection1[0]] - X[intersection2[0]])

def FWHM_gaussiasn (sigma):
    return 2*sigma*np.sqrt(2 * np.log(2))

def FWGM_lorentzian(gamma) :
    return 2*gamma

def FWGM_voigt(sigma,gamma):
    return(0.5346 *FWGM_lorentzian(gamma) + np.sqrt(0.2166*FWGM_lorentzian(gamma)**2 + FWHM_gaussiasn(sigma)))

def x_generator (halfwidth, halftheta) :
    return halfwidth / (np.tan(halftheta) * np.sin(halftheta))

def y_generator (halfwidth, halftheta) :
    return (halfwidth/np.tan(halftheta))**2

def Single_Voigt(x, alpha, gamma):
    sigma = alpha / np.sqrt(2 * np.log(2))
    return np.real(wofz((x + 1j*gamma)/sigma/np.sqrt(2))) / sigma/np.sqrt(2*np.pi)

def VoigtMaker(peaknum):
    if peaknum==8:
        def Voigt (x,expamp,expdec,a,b, cen1, ampV1,sigmaV1, gammaV1 , cen2, ampV2,sigmaV2, gammaV2 , cen3, ampV3,sigmaV3, gammaV3, cen4, ampV4,sigmaV4, gammaV4 , cen5, ampV5, sigmaV5, gammaV5, cen6, ampV6, sigmaV6, gammaV6 , cen7, ampV7, sigmaV7, gammaV7 , cen8, ampV8, sigmaV8, gammaV8):
            return expamp*exp(-x/expdec) + a*x +b +\
                   ampV1*  Single_Voigt(x-cen1,sigmaV1, gammaV1) + ampV2* Single_Voigt(x-cen2,sigmaV2, gammaV2) +ampV3* Single_Voigt(x-cen3,sigmaV3, gammaV3) +ampV4* Single_Voigt(x-cen4,sigmaV4, gammaV4) +\
                   ampV5* Single_Voigt(x-cen5,sigmaV5, gammaV5) + ampV6* Single_Voigt(x-cen6,sigmaV6, gammaV6) +ampV7* Single_Voigt(x-cen7,sigmaV7, gammaV7) +ampV8* Single_Voigt(x-cen8,sigmaV8, gammaV8)

    elif peaknum==7:
        def Voigt (x,expamp,expdec,a,b, cen1, ampV1,sigmaV1, gammaV1 , cen2, ampV2,sigmaV2, gammaV2 , cen3, ampV3,sigmaV3, gammaV3, cen4, ampV4,sigmaV4, gammaV4 , cen5, ampV5, sigmaV5, gammaV5, cen6, ampV6, sigmaV6, gammaV6 , cen7, ampV7, sigmaV7, gammaV7):
            return expamp*exp(-x/expdec) + a*x +b +\
                   ampV1*  Single_Voigt(x-cen1,sigmaV1, gammaV1) + ampV2* Single_Voigt(x-cen2,sigmaV2, gammaV2) +ampV3* Single_Voigt(x-cen3,sigmaV3, gammaV3) +ampV4* Single_Voigt(x-cen4,sigmaV4, gammaV4) +\
                   ampV5* Single_Voigt(x-cen5,sigmaV5, gammaV5) + ampV6* Single_Voigt(x-cen6,sigmaV6, gammaV6) +ampV7* Single_Voigt(x-cen7,sigmaV7, gammaV7)

    elif peaknum==6:
        def Voigt (x,expamp,expdec,a,b, cen1, ampV1,sigmaV1, gammaV1 , cen2, ampV2,sigmaV2, gammaV2 , cen3, ampV3,sigmaV3, gammaV3, cen4, ampV4,sigmaV4, gammaV4 , cen5, ampV5, sigmaV5, gammaV5, cen6, ampV6, sigmaV6, gammaV6):
            return expamp*exp(-x/expdec) + a*x +b +\
                   ampV1*  Single_Voigt(x-cen1,sigmaV1, gammaV1) + ampV2* Single_Voigt(x-cen2,sigmaV2, gammaV2) +ampV3* Single_Voigt(x-cen3,sigmaV3, gammaV3) +ampV4* Single_Voigt(x-cen4,sigmaV4, gammaV4) +\
                   ampV5* Single_Voigt(x-cen5,sigmaV5, gammaV5) + ampV6* Single_Voigt(x-cen6,sigmaV6, gammaV6)

    elif peaknum==5:
        def Voigt (x,expamp,expdec,a,b, cen1, ampV1,sigmaV1, gammaV1 , cen2, ampV2,sigmaV2, gammaV2 , cen3, ampV3,sigmaV3, gammaV3, cen4, ampV4,sigmaV4, gammaV4 , cen5, ampV5, sigmaV5, gammaV5):
            return expamp*exp(-x/expdec) + a*x +b +\
                   ampV1*  Single_Voigt(x-cen1,sigmaV1, gammaV1) + ampV2* Single_Voigt(x-cen2,sigmaV2, gammaV2) +ampV3* Single_Voigt(x-cen3,sigmaV3, gammaV3) +ampV4* Single_Voigt(x-cen4,sigmaV4, gammaV4) +\
                   ampV5* Single_Voigt(x-cen5,sigmaV5, gammaV5)

    elif peaknum==4:
        def Voigt (x,expamp,expdec,a,b, cen1, ampV1,sigmaV1, gammaV1 , cen2, ampV2,sigmaV2, gammaV2 , cen3, ampV3,sigmaV3, gammaV3, cen4, ampV4,sigmaV4, gammaV4 ):
            return expamp*exp(-x/expdec) + a*x +b +\
                   ampV1*  Single_Voigt(x-cen1,sigmaV1, gammaV1) + ampV2* Single_Voigt(x-cen2,sigmaV2, gammaV2) +ampV3* Single_Voigt(x-cen3,sigmaV3, gammaV3) +ampV4* Single_Voigt(x-cen4,sigmaV4, gammaV4)

    elif peaknum==3:
        def Voigt (x,expamp,expdec,a,b, cen1, ampV1,sigmaV1, gammaV1 , cen2, ampV2,sigmaV2, gammaV2 , cen3, ampV3,sigmaV3, gammaV3 ):
            return expamp*exp(-x/expdec) + a*x +b +\
                   ampV1*  Single_Voigt(x-cen1,sigmaV1, gammaV1) + ampV2* Single_Voigt(x-cen2,sigmaV2, gammaV2) +ampV3* Single_Voigt(x-cen3,sigmaV3, gammaV3)

    else:
        raise NameError("peak more than 8 or less than 3")
    
    return Voigt

def OutVoigtMaker(peaknum):
    if peaknum==5:
        def Voigt (x,a,b,c, cen1, ampV1,sigmaV1, gammaV1 , cen2, ampV2,sigmaV2, gammaV2 , cen3, ampV3,sigmaV3, gammaV3, cen4, ampV4,sigmaV4, gammaV4 , cen5, ampV5, sigmaV5, gammaV5):
            return a*x*x +b*x +c +\
                   ampV1*  Single_Voigt(x-cen1,sigmaV1, gammaV1) + ampV2* Single_Voigt(x-cen2,sigmaV2, gammaV2) +ampV3* Single_Voigt(x-cen3,sigmaV3, gammaV3) +ampV4* Single_Voigt(x-cen4,sigmaV4, gammaV4) +\
                   ampV5* Single_Voigt(x-cen5,sigmaV5, gammaV5)

    elif peaknum==4:
        def Voigt (x,a,b,c,cen1, ampV1,sigmaV1, gammaV1 , cen2, ampV2,sigmaV2, gammaV2 , cen3, ampV3,sigmaV3, gammaV3, cen4, ampV4,sigmaV4, gammaV4 ):
            return a*x*x +b*x +c +\
                   ampV1*  Single_Voigt(x-cen1,sigmaV1, gammaV1) + ampV2* Single_Voigt(x-cen2,sigmaV2, gammaV2) +ampV3* Single_Voigt(x-cen3,sigmaV3, gammaV3) +ampV4* Single_Voigt(x-cen4,sigmaV4, gammaV4)

    elif peaknum==3:
        def Voigt (x,a,b,c,cen1, ampV1,sigmaV1, gammaV1 , cen2, ampV2,sigmaV2, gammaV2 , cen3, ampV3,sigmaV3, gammaV3 ):
            return a*x*x +b*x +c +\
                   ampV1*  Single_Voigt(x-cen1,sigmaV1, gammaV1) + ampV2* Single_Voigt(x-cen2,sigmaV2, gammaV2) +ampV3* Single_Voigt(x-cen3,sigmaV3, gammaV3)

    elif peaknum==2:
        def Voigt (x,a,b,c,cen1, ampV1,sigmaV1, gammaV1 , cen2, ampV2,sigmaV2, gammaV2 ):
            return a*x*x +b*x +c +\
                   ampV1*  Single_Voigt(x-cen1,sigmaV1, gammaV1) + ampV2* Single_Voigt(x-cen2,sigmaV2, gammaV2)

    elif peaknum==1:
        def Voigt (x,a,b,c, cen1, ampV1,sigmaV1, gammaV1 ):
            return a*x*x +b*x +c +\
                   ampV1*  Single_Voigt(x-cen1,sigmaV1, gammaV1)

    else:
        raise NameError("peak more than 5")
    
    return Voigt