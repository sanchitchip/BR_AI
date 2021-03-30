# BR AI and Automation Lab: Satellite Imagery

## Project Description

The Goal of this Project was to locate Urban Heat Islands in a given City, and to analyse their development over time, as well as the corresponding development of vegetation and soil moisture for the located areas. For this purpose, a data pipeline that can fetch batches of satellite imagery on arbitrary locations and timeframes was built. After fetching data, functions for calculating the metrics of interest (i.e. [Landsurface Temperature](https://www.usgs.gov/core-science-systems/nli/landsat/using-usgs-landsat-level-1-data-product), [NDVI](https://labo.obs-mip.fr/multitemp/using-ndvi-with-atmospherically-corrected-data/) and [NDWI](https://en.wikipedia.org/wiki/Normalized_difference_water_index)) is applied. In the next Step, a function utilizing a [DoH-Algorithm](https://scikit-image.org/docs/dev/auto_examples/features_detection/plot_blob.html) is used to detect possible Heat Islands. Finally, we can call an interactive Dash App to visualize the detected Heat Island candidates on a map together with their corresponding metrics and their devolopment over time.  

## Code Workflow 

## Dash App Interface 

## Definition and Detection of Heat Islands
The DoH Algorithm detects locations, where changes in the determinant of the Hessian Matrix (which corresponds to local maxima or minima in curvature) lie above a a certain threshhold. This gives a number of candidates for potential Heat Islands. In the next step, we compare the temperature of each heat island candidate to the 0.98-Quantile of temperature of the surrounding area, and classify a candidate as Heat Island, only if it lies above the 0.98-Quantile value. This ensures we get rid of local minima and larger areas that have a high Landssurface Temperature in general. As there is no widely accepted definition of what constitutes a heat island, it might be of interest for any future usage to vary this defintion, which can be done by altering the following parameters of the `island_detection` in the *lst.py* file: 

* `threshold=0.1` This Parameter controls the threshold of what is considered a significant change in temperature. **Reduce this to detect less prominent blobs**.
* `max_sigma` This parameter controls the maximum standard deviation for Gaussian Kernel used to compute Hessian matrix. **Keep this high to detect larger blobs**.
* `min_sigma` This parameter controls the minimum standard deviation for Gaussian Kernel used to compute Hessian matrix.. **Keep this low to detect smaller blobs.**.



## Demo 
