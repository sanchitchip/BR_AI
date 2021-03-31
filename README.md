# BR AI and Automation Lab: Satellite Imagery

## Project Description

The Goal of this Project was to create a tool that allows to locate Urban Heat Islands in a given City along with an analysis of their development over time, as well as the corresponding development of vegetation and soil moisture for the located areas. For this purpose, a data pipeline that can fetch batches of satellite imagery on arbitrary locations and timeframes was built. After fetching data, functions for calculating the metrics of interest (i.e. [Landsurface Temperature](https://www.usgs.gov/core-science-systems/nli/landsat/using-usgs-landsat-level-1-data-product), [NDVI](https://labo.obs-mip.fr/multitemp/using-ndvi-with-atmospherically-corrected-data/) and [NDWI](https://en.wikipedia.org/wiki/Normalized_difference_water_index)) is applied. After calculation of the LST a [DoH-Algorithm](https://scikit-image.org/docs/dev/auto_examples/features_detection/plot_blob.html) is used to detect possible Heat Islands. Finally, we can call an interactive Dash App to visualize the detected Heat Island candidates on a map together with their corresponding metrics and their devolopment over time.  

## Code Workflow 
Following is a short description of the succession of the code workflow and each function:

1. `io_pipe.py` Contains functions to fetch Landsat8 images via the [Sentinelhub API](https://www.sentinel-hub.com/). Timeframe and Area of interest can be specified. The default area is Munich.  
2. `lst.py` Contains functions to calculate Landsurface Temperature and detect possible heat islands on a given batch of data. 
3. `get_coord.py` Contains functions to provide the coordinates of the heat islands candidates as located by *lst.py*, which are necessary for the dash app. 
4. `nd_index.py` Contains functions to calculate NDVI and NDWI. 
5. `aggregate.py` Contains functions to aggregate the data and the calculated metrics for the dash app.
6. `app.py` Contains functionality to build the dash app and visualize the results interactively. 

## Dash App Interface 
![alt text](https://github.com/sanchitchip/BR_AI/blob/main/Interface.jpeg)
On the left side of the Interface a map of the area of interest is displayed. It shows all detected heat island candidates as red squares. It is possible to zoom in on the map to check locations in detail. Each Red Square is selectable. When selected, detailed information reagrding the respective Heat Island Candidate is displayed on the right sight of the interface. <br><br>
In the middle of the right side, a close up view on the selected area is displayed. The three filter boxes `NDVI`, `NDWI` and `LST` determine which metric is displayed. This can be used to check the structure and form of a possible heat island. The slider on top can be used to switch between years, which allows for an examination of the development of the selected area over time. At the bottom, a time series graph is displayed for the selected metric over the whole timeframe. 

## Definition and Detection of Heat Islands
The DoH Algorithm detects locations, where changes in the determinant of the Hessian Matrix (which corresponds to local maxima or minima in curvature) lie above a a certain threshhold. This gives a number of candidates for potential Heat Islands. In the next step, we compare the temperature of each heat island candidate to the 0.98-Quantile of temperature of the surrounding area, and classify a candidate as Heat Island, only if it lies above the 0.98-Quantile value. This ensures we get rid of local minima and larger areas that have a high Landssurface Temperature in general. As there is no widely accepted definition of what constitutes a heat island, it might be of interest for any future usage to vary this defintion, which can be done by altering the following parameters of the `island_detection()` function in the *lst.py* file: 

* `threshold` This Parameter controls the threshold of what is considered a significant change in temperature. **Reduce this to detect less prominent locations**.
* `max_sigma` This parameter controls the maximum standard deviation for Gaussian Kernel used to compute Hessian matrix. **Keep this high to detect larger locations**.
* `min_sigma` This parameter controls the minimum standard deviation for Gaussian Kernel used to compute Hessian matrix. **Keep this low to detect smaller locations**.

Other parameters to alter the defintion and detection process would be changing the 0.98-Quantile to a different value, as well as the comparison area it is applied to. The default is set to a 20 * 20 pixel box. Both parameters are included in the `temperature_threshold()` function of the *lst.py* file. For (visual) examples on the detection workflow, see `Heat_island_detection.ipynb` in the examples folder. 

## Demo 
code demo or reference to notebook

## What else to know 
The whole workflow as described under Code and Workflow can easily be generalized to arbitrary locations and timeframes. However it is important to note that the quality of the Analysis is limited by the quality of the Data. Concretly speaking, with public Landsat8 data it is hard to conduct a plausible timeseries analysis. Therefore this tool is to be seen as an exploratory tool, that can support with finding points of interest for further (external) analysis. For further information, see also the attached slides under `Final_Presentation.pdf`. 
