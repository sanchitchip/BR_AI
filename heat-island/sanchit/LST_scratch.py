import os
import arcgis
import numpy as np
import pdb
import rasterio
from rasterio.plot import show
vfile = "12.09.2016/"
B4 = vfile+"B4.TIF"
B5 = vfile+"B5.TIF"
B10 = vfile+"B10.TIF"
B11 = vfile+"B11.TIF"

B4 = rasterio.open(B4)
B5 = rasterio.open(B5)
B10 = rasterio.open(B10)
B11 = rasterio.open(B11)
B4 = B4.read(1).astype(float)
B5 = B5.read(1).astype(float)
B10 = B10.read(1).astype(float)
B11 = B11.read(1).astype(float)

metadata = vfile+ "LC08_L1TP_192027_20160912_20200906_02_T1_MTL.txt"

scrap_lines = []

with open(metadata, 'r') as list_file:
   for x in list_file:
       if 'DATE_ACQUIRED' in x:
           scrap_lines.append(x.rstrip('\n').strip())
       if 'SCENE_CENTER_TIME' in x:
           scrap_lines.append(x.rstrip('\n').strip())
       if 'SUN_ELEVATION' in x:
           scrap_lines.append(x.rstrip('\n').strip())
       if 'REFLECTANCE_MULT_BAND_4' in x:
           scrap_lines.append(x.rstrip('\n').strip())
       if 'REFLECTANCE_ADD_BAND_4' in x:
           scrap_lines.append(x.rstrip('\n').strip())
       if 'REFLECTANCE_MULT_BAND_5' in x:
           scrap_lines.append(x.rstrip('\n').strip())
       if 'REFLECTANCE_ADD_BAND_5' in x:
           scrap_lines.append(x.rstrip('\n').strip())
       if 'RADIANCE_MULT_BAND_10' in x:
           scrap_lines.append(x.rstrip('\n').strip())
       if 'RADIANCE_MULT_BAND_11' in x:
           scrap_lines.append(x.rstrip('\n').strip())
       if 'RADIANCE_ADD_BAND_10' in x:
           scrap_lines.append(x.rstrip('\n').strip())
       if 'RADIANCE_ADD_BAND_11' in x:
           scrap_lines.append(x.rstrip('\n').strip())
       if 'K1_CONSTANT_BAND_10' in x:
           scrap_lines.append(x.rstrip('\n').strip())
       if 'K2_CONSTANT_BAND_10' in x:
           scrap_lines.append(x.rstrip('\n').strip())
       if 'K1_CONSTANT_BAND_11' in x:
           scrap_lines.append(x.rstrip('\n').strip())
       if 'K2_CONSTANT_BAND_11' in x:
           scrap_lines.append(x.rstrip('\n').strip())

scrap_lines_clean = []

for x in scrap_lines:
   scrap_lines_clean.append(x.split('=')[1].strip())

DATE_ACQUIRED = scrap_lines_clean[0].replace('-', '')
SCENE_CENTER_TIME1 = scrap_lines_clean[1][1:-1]
SCENE_CENTER_TIME = SCENE_CENTER_TIME1.split('.')[0].replace(':', '')
SUN_ELEVATION = float(scrap_lines_clean[2])
RADIANCE_MULT_BAND_10 = float(scrap_lines_clean[3])
RADIANCE_MULT_BAND_11 = float(scrap_lines_clean[4])
RADIANCE_ADD_BAND_10 = float(scrap_lines_clean[5])
RADIANCE_ADD_BAND_11 = float(scrap_lines_clean[6])
REFLECTANCE_MULT_BAND_4 = float(scrap_lines_clean[7])
REFLECTANCE_MULT_BAND_5 = float(scrap_lines_clean[8])
REFLECTANCE_ADD_BAND_4 = float(scrap_lines_clean[9])
REFLECTANCE_ADD_BAND_5 = float(scrap_lines_clean[10])
K1_CONSTANT_BAND_10 = float(scrap_lines_clean[11])
K2_CONSTANT_BAND_10 = float(scrap_lines_clean[12])
K1_CONSTANT_BAND_11 = float(scrap_lines_clean[13])
K2_CONSTANT_BAND_11 = float(scrap_lines_clean[14])

#Correct Sun Elevation
sin_sun_elev = np.sin(np.deg2rad(SUN_ELEVATION))
corrected_sun_elev = float(sin_sun_elev)

#Calculate Red Band and NIR band, corrected with sun elevation. Create NDVI based off of these rasters
RED_REF = ((REFLECTANCE_MULT_BAND_4 * B4) - REFLECTANCE_ADD_BAND_4) / (corrected_sun_elev)
NIR_REF = ((REFLECTANCE_MULT_BAND_5 * B5) - REFLECTANCE_ADD_BAND_5) / (corrected_sun_elev)
#pdb.set_trace()

NDVI_REF = (NIR_REF - RED_REF) / (NIR_REF + RED_REF)
#Create variables for the NDVI's max and min values:
NDVI_min = np.min(NDVI_REF)

NDVI_max = np.max(NDVI_REF)



#Using band 10 and 11, calculate radiance and brightness temp:
BAND_10_RADIANCE = (RADIANCE_MULT_BAND_10 * B10) + RADIANCE_ADD_BAND_10
BAND_11_RADIANCE = (RADIANCE_MULT_BAND_11 * B11) + RADIANCE_ADD_BAND_11

BAND10SATTEMP = ((K2_CONSTANT_BAND_10 / np.log((K1_CONSTANT_BAND_10/BAND_10_RADIANCE + 1)) - 272.15))
BAND11SATTEMP = ((K2_CONSTANT_BAND_11 / np.log((K1_CONSTANT_BAND_11/BAND_11_RADIANCE + 1)) - 272.15))

#Calculate Prop VEG using NDVI's min max, Use propveg to calculate the LSE:
PROPVEG = np.square((NDVI_REF - NDVI_min) / (NDVI_max - NDVI_min))

LSE = (0.004 * PROPVEG) + 0.986

#Use the LSE to estimate the LST of band 10, 11:
BAND10LST = (BAND10SATTEMP / 1) + (B10 * (BAND10SATTEMP/14380) * (np.log(LSE)))
BAND11LST = (BAND11SATTEMP / 1) + (B11 * (BAND11SATTEMP/14380) *  (np.log(LSE)))

#Find mean LST:
LST_MEAN_11_10 = (BAND10LST + BAND11LST)/2

show(LST_MEAN_11_10)
