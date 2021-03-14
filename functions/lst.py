import numpy as np

def BrightnessTemp(B, ADD_BAND, MULT_BAND, k1, k2):
    # Reference: https://www.usgs.gov/core-science-systems/nli/landsat/using-usgs-landsat-level-1-data-product
    vRad = (MULT_BAND * B) + ADD_BAND
    vTemp = ((k2 / np.log((k1 / vRad + 1)) - 272.15))
    return vTemp


def LSE(NDVI):
    vEm = np.zeros(NDVI.shape)

    h, i, j = np.where(NDVI < 0.2)
    vEm[h, i, j] = 0.97

    z, k, l = np.where(NDVI > 0.5)
    vEm[z, k, l] = 0.99
    x, m, n = np.where((NDVI >= 0.2) & (NDVI <= 0.5))
    vEm[x, m, n] = (0.004 * (((NDVI[x, m, n] - 0.2) / (0.5 - 0.2)) ** 2)) + 0.986

    return vEm

def mono_LST(B_TEMP, B_LSE):
    # old way to compute LST
    # B_LST = (B_TEMP / 1) + (B10 * (B_TEMP/14380) * (np.log(B_LSE)))
    ## BETTER way to computer the LST.
    B_LST = B_TEMP / (1 + (((0.0000115 * B_TEMP) / 14380) * np.log(B_LSE)))
    return B_LST



# vtime = []
# vcc = .2
# for idx in range(len(vtime_interval)):
#     try:
#         vtime.append(validate_timestamp(time_interval=vtime_interval[idx],
#                        config=vconfig,
#                        maxcc=vcc))
#     except:
#         print("No image exists for the parameters: time interval {},cloud coverage: {},".format(i,vcc))



def temperature_threshold(vdesired, blobs):
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