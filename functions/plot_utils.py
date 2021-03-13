import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import logging
from matplotlib.colors import Normalize


def plot_ndi(image, factor=1.0, clip_range=None, is_bar=True, **kwargs):
    """
    Utility function for plotting Normalized Difference Index images.
    
    Args:
        param factor: factor to rescale image.
        type factor: float.
        
        param clip_range: range to clip image.
        type clip_range: float.
        
        param is_bar: whether to plot colorbar.
        type is_bar: bool.
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))
    if clip_range is not None:
        im = ax.imshow(np.clip(image * factor, *clip_range), **kwargs)
    else:
        im = ax.imshow(image * factor, **kwargs)
    if is_bar:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(im, cax=cax)
    ax.set_xticks([])
    ax.set_yticks([])
    

def plot_truecolor(image, factor=2.5, clip_range=[0,1],is_bar=False):
    """
    Utility function for plotting Normalized Difference Index images.
    
    Args:
        param factor: factor to rescale image.
        type factor: float.
        
        param clip_range: range to clip image.
        type clip_range: float.
        
        param is_bar: whether to plot colorbar.
        type is_bar: bool.
    """
    
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))
    if clip_range != None:
        im = ax.imshow(np.clip(image[...,[3,2,1]] * factor, *clip_range), vmin=0, vmax=1)
    else:
        im = ax.imshow(image[...,[3,2,1]])
    if is_bar:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        fig.colorbar(im, cax=cax)
    ax.set_xticks([])
    ax.set_yticks([])
    
# testing ideas:
# 1.) check input arguments data type
# 2.) check if any inputs arguments are None and if yes return value error
def plot_LST_true(True_Image,LST,date,cmp=None):
    """
    Function which plots satellite image and its corresponding land surface temperature as subplots.
    Args:
        param True_Image: numpy array(RGB) of satellite image of shape (h,w,3) 
        type factor: np.array.
        
        param LST: LST matrix of the corresponding satellite image of shape (h,w).
        type LST: np.array.
        
        param date: timestamp info of the satellite image so can be added in the plot.
        type is_bar: datetime.datetime .
        
        param cmap: colormap for the plot. If None looks at the max and min value of the LST matrix
        type cmap: matplotlib cmap object
        
    """    
    
    # to remove the clipping warning/logging. 
    logger = logging.getLogger()
    old_level = logger.level
    logger.setLevel(100)
    ## the above part is only to remove the clipping warning and has no other relevance to the plot code.
    if cmp is not None:
        norm = Normalize(vmin=cmp[0],vmax=cmp[1])        
    else:
        norm = Normalize(vmin=np.min(LST),vmax=np.max(LST))        

    plt.rcParams['figure.figsize'] = [12, 8]    
    f, (ax1,ax2) = plt.subplots(1,2)
    im = ax2.imshow(LST,cmap=plt.cm.jet,norm=norm)
    f.colorbar(im,orientation="horizontal",fraction=0.07)
    ax1.imshow(True_Image)
    ax1.set_title(date)
    plt.show()

def plot_all_LST(True_Image,LST,date):
    """
    Function which plots all satellite image and there corresponding land surface temperature. 
    This function will only work for Jupyter Notebooks for .py u will have to write subplots.
    Args:
        param True_Image: numpy array(RGB) of satellite image of shape (n,h,w,3) where n is number of images
        type factor: np.array.
        
        param LST: LST matrix of the corresponding satellite image of shape (n,h,w). where n is number of images
        type LST: np.array.
        
        param date: timestamp info of the satellite image so can be added in the plot.
        type is_bar: datetime.datetime .        
    """
    
    vmax = np.max(LST)
    vmin = np.min(LST)
    cmp = (vmax,vmin)
    assert True_Image.shape[:-1] == LST.shape
    vSze = True_Image.shape[0]
    for i in range(vSze):
        plot_LST_true(True_Image[i],LST[i],date[i],cmp = None )

def plot_islands(original,lst,detected_island,limit=None,enhance_radius=False):
    """
    Function which plots all satellite image and there corresponding land surface temperature. 
    This function will only work for Jupyter Notebooks for .py u will have to write subplots.
    Args:
        param original: numpy array(RGB) of satellite image of shape (n,h,w,3) where n is number of images
        type factor: np.array.
        
        param LST: LST matrix of the corresponding satellite image of shape (n,h,w). where n is number of images
        type LST: np.array.
        
        param detected_island: list of the coordinates of detected island which are to be plotted in the original 
        and its corresponding image.
        type detected_island:  list of tuple.
        
        param enhance_radius: whether to plot circle with bigger radius instead of the one computed by hessian algorithm.
        type enhance_radius: boolean  .
        
    """
    
    fig, axes = plt.subplots(1, 2, figsize=(40, 40), sharex=True, sharey=True)
    ax = axes.ravel()
    #plt.imshow(vLST[0],cmap='gray')
    ax[0].imshow(original)
    ax[1].imshow(lst,cmap=plt.cm.jet)
    for blob in detected_island:
        y, x, r = blob
        if limit is None:
            if enhance_radius:
                c = plt.Circle((x, y), r*3, color='green', linewidth=2, fill=False)
            else:
                c =plt.Circle((x, y), r, color='green', linewidth=2, fill=False)
            c2 = plt.Circle((x, y), r, color='green', linewidth=2, fill=False)
            ax[0].add_patch(c)
            ax[1].add_patch(c2)
        else:            
            if r>limit:
                if enhance_radius:
                    print("here")
                    c = plt.Circle((x, y), r*3, color='green', linewidth=2, fill=False)
                else:
                    c =plt.Circle((x, y), r, color='green', linewidth=2, fill=False)
                c2 = plt.Circle((x, y), r, color='green', linewidth=2, fill=False)
                ax[0].add_patch(c)
                ax[1].add_patch(c2)
    plt.show()