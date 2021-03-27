import numpy as np

def BrightnessTemp(B, ADD_BAND, MULT_BAND, k1, k2):
    # Reference: https://www.usgs.gov/core-science-systems/nli/landsat/using-usgs-landsat-level-1-data-product
    """ This functions returns Brightness temperature which is useful for computation of Land surface temperature.
    Args:
        param B: numpy array 
        type B: int.

        param ADD_BAND: Band-specific thermal conversion constant from the metadata .
        type ADD_BAND: int or float.
        
        param MULT_BAND: Band-specific thermal conversion constant from the metadata.
                
        type MULT_BAND: int or float
        
        param k1: Band-specific thermal conversion constant from the metadata 
                          (K1_CONSTANT_BAND_x, where x is the thermal band number)
        param k1: Band-specific thermal conversion constant from the metadata 
                   (K2_CONSTANT_BAND_x, where x is the thermal band number)
        
    Returns: 
         returns the brightness temperature matrix(Kelvin) for the given satellite image.
    """
    
    # vRad = TOA spectral radiance (Watts/( m2 * srad * μm))
    vRad = (MULT_BAND * B) + ADD_BAND
    vTemp = ((k2 / np.log((k1 / vRad + 1)) - 272.15))
    return vTemp


def LSE(NDVI):
    """ This functions returns Land surface emissivity which is useful for computation of Land surface temperature.
    Args:
        param NDVI: Vegetation index  
        type NDVI: numpy array
        
    Returns: 
         returns the brightness temperature matrix(Kelvin) for the given satellite image.
    """
    if not isinstance(NDVI,np.ndarray):
        raise TypeError('Please provide a  Numpy array for NDVI')

    ## will add values for emmisivity in the zero array
    vEm = np.zeros(NDVI.shape)
    ## one of the standard algorithm used to calculate LSE.
    h, i, j = np.where(NDVI < 0.2)
    vEm[h, i, j] = 0.97

    z, k, l = np.where(NDVI > 0.5)
    vEm[z, k, l] = 0.99
    x, m, n = np.where((NDVI >= 0.2) & (NDVI <= 0.5))
    vEm[x, m, n] = (0.004 * (((NDVI[x, m, n] - 0.2) / (0.5 - 0.2)) ** 2)) + 0.986

    return vEm

def mono_LST(B_TEMP, B_LSE):
    """ This functions returns Land surface temperature(Kelvin) for a satellite image computed using Mono-window algorithm
        using brightness temperature matrix
        and land surface emissivity matrix.
    Args:
        param B_TEMP: Brightness temperature matrix returned from either the Brightness temperature function or directly fetched 
                       using sentinel hub API
        type B_TEMP: numpy array

        param B_LSE: Surface emmisivity matrix returned from LSE function. 
        type B_LSE: numpy array
        
    Returns: Land surface temperautre matrix.
    
    """
    if not isinstance(B_TEMP,np.ndarray):
        raise TypeError('Please provide a  Numpy array for Brightness Temperature')

    if not isinstance(B_LSE,np.ndarray):
        raise TypeError('Please provide a  Numpy array for LSE')

    if B_TEMP.shape != B_LSE.shape:
        raise ValueError("Brightness temperature and LSE have different shape.")
    # old way to compute LST
    # B_LST = (B_TEMP / 1) + (B10 * (B_TEMP/14380) * (np.log(B_LSE)))
    ## BETTER way to computer the LST.
    B_LST = B_TEMP / (1 + (((0.0000115 * B_TEMP) / 14380) * np.log(B_LSE)))
    return B_LST


def temperature_threshold(vdesired, blobs):
    """ This function acts as a threshold to remove unwanted detected island which are of low temperature by 
        taking a 20*20 patch and computing its mean which if is above a threshold(98 percentile of LST temperature) than selected 
        that.
    Args:
        param vdesired: LST matrix
        type B_TEMP: numpy array

        param blobs: list of island candidates generated using any othe the implemented algorithm (DOH,DOG etc..) 
        type blobs: list of tuple.
        
    Returns: returns numpy array of potential island candidates after threshold.
    
    """
    if not isinstance(vdesired,np.ndarray):
        raise TypeError('Please provide a  Numpy array for vdesired')
 
    if not isinstance(blobs,list):
        raise TypeError('Please provide a list of tuples for blobs')

    vfinal = []
    vrange = 10
    vper = np.percentile(vdesired, q=98)
    for blob in blobs:
        y, x, r = blob
        y, x = y.astype(np.int64), x.astype(np.int64)
        #     vmean = vdesired[x-vrange:x+vrange,y-vrange:y+vrange].mean()
        vmean = vdesired[y - vrange:y + vrange, x - vrange:x + vrange].mean()
        if vmean > vper:
            vfinal.append(np.array([y, x, r]))
    vfinal = np.array(vfinal)
    return vfinal


'''
taking a patch of 30x30 pixel for each possible blob 
and seeing if the average temperature is greater than 90th percentile of the temperature
''' 
def threshold_hessian(desired,blobs,filter_size=10):
    """ This function acts as a threshold to remove unwanted detected island which are of low temperature by 
        taking a 20*20 patch and computing its mean which if is above a threshold(98 percentile of LST temperature) than selected 
        that.
    Args:
        param vdesired: LST matrix
        type B_TEMP: numpy array

        param blobs: list of island candidates generated using any othe the implemented algorithm (DOH,DOG etc..) 
        type blobs: list of tuple.
        
    Returns: returns numpy array of potential island candidates after threshold.
    
    """
    vfinal= []
    vrange=filter_size
    vper = np.percentile(desired,q=98)
    for blob in blobs:
        y,x,r = blob
        y,x = y.astype(np.int64),x.astype(np.int64)
    #     vmean = vdesired[x-vrange:x+vrange,y-vrange:y+vrange].mean()
        vmean = desired[y-vrange:y+vrange,x-vrange:x+vrange].mean()
        if vmean>vper:
            vfinal.append(np.array([y,x,r]))
    vfinal = np.array(vfinal)
    return vfinal

