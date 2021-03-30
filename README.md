# BR AI and Automation Lab: Satellite Imagery

## Project Description

The Goal of this Project was to locate Urban Heat Islands in a given City, and to analyse their development over time, as well as the corresponding development of vegetation and soil moisture for the located areas. For this purpose, a data pipeline that can fetch batches of satellite imagery on arbitrary locations and timeframes was built. After fetching data, functions for calculating the metrics of interest (i.e. [Landsurface Temperature](https://www.usgs.gov/core-science-systems/nli/landsat/using-usgs-landsat-level-1-data-product), [NDVI](https://labo.obs-mip.fr/multitemp/using-ndvi-with-atmospherically-corrected-data/) and [NDWI](https://en.wikipedia.org/wiki/Normalized_difference_water_index)) can be applied. In the next Step, a function utilizing a [DoH-Algorithm] (https://scikit-image.org/docs/dev/auto_examples/features_detection/plot_blob.html) is used to detect possible Heat Islands.

