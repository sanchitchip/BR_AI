import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable


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
    


