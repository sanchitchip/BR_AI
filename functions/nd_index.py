import numpy as np

def normalized_difference_index(band_a, band_b, c=0):
    """
    Calculates a Normalized Difference Index (NDI) between two bands A and B as
    NDI = (A - B + c)/(A + B + c), where c is provided as the acorvi_constant argument.
    For the reasoning behind using the acorvi_constant in the equation, check the article
    Using NDVI with atmospherically corrected data(https://labo.obs-mip.fr/multitemp/using-ndvi-with-atmospherically-corrected-data/).
    
    Args:
        param band_a, band_b: Original Data of one band.
        type eopatch_data: 3d np.ndarray, shape(time,image_width,image_height).
        
        param c: acorvi_constant argument.
        type c: float.
    """

    ndi = np.divide((band_a - band_b + c), (band_a + band_b + c))
    ndi = np.nan_to_num(ndi)
    return ndi


def calc_ndvi(eopatch_data, satellite='landsat8', c=0):
    """
    Calculates Normalized difference vegetation index.
    NDVI is a simple, but effective index for quantifying green vegetation.
    It normalizes green leaf scattering in Near Infra-red wavelengths with chlorophyll absorption in red wavelengths.
    NDVI = (NIR - RED) / (NIR + RED)
    Note: The value range of the NDVI is -1 to 1.
    Negative values of NDVI (values approaching -1) correspond to water.
    Values close to zero (-0.1 to 0.1) generally correspond to barren areas of rock, sand, or snow.
    Low, positive values represent shrub and grassland (approximately 0.2 to 0.4),
    while high values indicate temperate and tropical rainforests (values approaching 1).
    It is a good proxy for live green vegetation.
    
    Args:
        param eopatch_data: Original Data tensor.
        type eopatch_data: np.ndarray, shape(time,image_width,image_height, bands).
        
        param satellite: Satellite Name.
        type satellite: str, 'landsat8', 'landsat5', 'landsat7' or 'sentinel'.
        
        param c: acorvi_constant argument.
        type c: float.
    return: ndvi
    """
    satellite = satellite.lower()

    if satellite not in ['landsat8', 'landsat5', 'landsat7', 'sentinel']:
        raise ValueError(f'{satellite} is not in the list')

    if satellite == 'landsat8':
        _nir_band = eopatch_data[:, :, :, 4]
        _red_band = eopatch_data[:, :, :, 3]

    if satellite == 'landsat5' or 'landsat7':
        _nir_band = eopatch_data[:, :, :, 3]
        _red_band = eopatch_data[:, :, :, 2]

    if satellite == 'sentinel':
        _nir_band = eopatch_data[:, :, :, 7]
        _red_band = eopatch_data[:, :, :, 3]

    ndvi = normalized_difference_index(_nir_band, _red_band, c=c)

    return ndvi



def calc_ndwi(eopatch_data, satellite='landsat8', c=0):
    """
    Calculates Normalized Difference Water Index.
    The NDWI is used to monitor changes related to water content in water bodies.
    As water bodies strongly absorb light in visible to infrared electromagnetic spectrum,
    NDWI uses green and near infrared bands to highlight water bodies.
    It is sensitive to built-up land and can result in over-estimation of water bodies.
    
    NDWI = (Green - NIR) / (Green + NIR)
    Note: Values description: Index values greater than 0.5 usually correspond to water bodies.
    Vegetation usually corresponds to much smaller values and built-up areas to values between zero and 0.2.
    NDWI index is often used synonymously with the NDMI index, often using NIR-SWIR combination as one of the two options.
    NDMI seems to be consistently described using NIR-SWIR combination.
    As the indices with these two combinations work very differently, with NIR-SWIR highlighting differences in water content of leaves, and GREEN-NIR highlighting differences in water content of water bodies, we have decided to separate the indices on our repository as NDMI using NIR-SWIR, and NDWI using GREEN-NI
    
    
     Args:
        param eopatch_data: Original Data tensor.
        type eopatch_data: np.ndarray, shape(time,image_width,image_height, bands).
        
        param satellite: Satellite Name.
        type satellite: str, 'landsat8', 'landsat5', 'landsat7' or 'sentinel'.
        
        param c: acorvi_constant argument.
        type c: float.
    return: ndvi
    """
    satellite = satellite.lower()

    if satellite not in ['landsat8', 'landsat5', 'landsat7', 'sentinel']:
        raise ValueError(f'{satellite} is not in the list')

    if satellite == 'landsat8':
        _green_band = eopatch_data[:, :, :, 2]
        _nir_band = eopatch_data[:, :, :, 4]

    if satellite == 'sentinel':
        _green_band = eopatch_data[:, :, :, 2]
        _nir_band = eopatch_data[:, :, :, 7]

    ndwi = normalized_difference_index(_green_band, _nir_band, c=c)

    return ndwi
