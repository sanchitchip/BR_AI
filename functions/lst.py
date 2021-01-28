import numpy as np

def BrightnessTemp(B, ADD_BAND, MULT_BAND, k1, k2):
    # Reference: https://www.usgs.gov/core-science-systems/nli/landsat/using-usgs-landsat-level-1-data-product
    vRad = (MULT_BAND * B) + ADD_BAND
    vTemp = ((k2 / np.log((k1 / vRad + 1)) - 272.15))
    return vTemp


def LSE(NDVI):
    vEm = np.zeros(NDVI.shape)

    i, j = np.where(NDVI < 0.2)
    vEm[i, j] = 0.97

    k, l = np.where(NDVI > 0.5)
    vEm[k, l] = 0.99
    m, n = np.where((NDVI >= 0.2) & (NDVI <= 0.5))
    vEm[m, n] = (0.004 * (((NDVI[m, n] - 0.2) / (0.5 - 0.2)) ** 2)) + 0.986

    return vEm


def mono_LST(B_TEMP, B_LSE):
    # old way to compute LST
    # B_LST = (B_TEMP / 1) + (B10 * (B_TEMP/14380) * (np.log(B_LSE)))
    ## BETTER way to computer the LST.
    B_LST = B_TEMP / (1 + (((0.0000115 * B_TEMP) / 14380) * np.log(B_LSE)))
    return B_LST