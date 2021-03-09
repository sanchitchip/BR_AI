#!/usr/bin/env python
# coding: utf-8

# In[1]:


## add the sys function part else there will be file loading errors.
import sys
import warnings
sys.path.insert(1,'../functions')
warnings.filterwarnings("ignore", category=DeprecationWarning) 


# In[2]:


import numpy as np
import io_pipe
import nd_index
import lst
import plot_utils
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
import logging
from eolearn.io import get_available_timestamps
import pdb
import geopandas as gpd


# In[3]:


from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray
from sklearn.preprocessing import scale
import pdb

# In[4]:


#get_ipython().run_line_magic('matplotlib', 'inline')


# In[5]:


## add your sentinelhub credentials to start running this.
config_dict = {
            'INSTANCE_ID': None,
            'CLIENT_ID': None,
            'CLIENT_SECRET': None
        }


# In[6]:


config_dict = {
            'INSTANCE_ID': '82f63741-572a-451c-905d-bd2575f2aad0',
            'CLIENT_ID': '4cac505f-9177-4874-ac2b-13c38b8ff178',
            'CLIENT_SECRET': ')5b0-PQyF%auI,8u>7Mv~^YhYJLMd_98Xe3>eeo5'
        }


# ##### replace the None from confing dictionary.

# In[7]:


vconfig = io_pipe.set_config(new_id=True,INSTANCE_ID=config_dict['INSTANCE_ID'],
                            CLIENT_ID= config_dict['CLIENT_ID'],
                            CLIENT_SECRET=config_dict['CLIENT_SECRET'])


# In[14]:


year_range = range(2014,2016)
date_range = [1,30]
month_range = [6,9]


# In[15]:


eopatch_data,vtimestamp = io_pipe.get_landsat8_range(config = vconfig,year_range=year_range,month=month_range,
                           date_range=date_range,maxcc=.2)


# In[16]:


NDVI_REF = nd_index.calc_ndvi(eopatch_data)


# In[17]:


B10 = eopatch_data[:,:,:,9]-273
B11 = eopatch_data[:,:,:,10]-273
#RADIANCE_ADD_BAND_10 = 0.10000
#RADIANCE_MULT_BAND_10 = 3.3420E-04
#K1_CONSTANT_BAND_10 = 774.8553
#K2_CONSTANT_BAND_10 = 1321.0789


# In[18]:


vLSE = lst.LSE(NDVI_REF)
vLST = lst.mono_LST(B10,vLSE)


# In[19]:


## use datamask for plot/NDVI/LST.
vR = eopatch_data[:,:,:,3]
vG = eopatch_data[:,:,:,2]
vB = eopatch_data[:,:,:,1]
vImg = np.stack([vR,vG,vB],axis =3)
vImg = (vImg *(255/  np.max(vImg))).astype(np.uint8)
vImg = (vImg*(3.5/255))


# In[20]:


#plot_utils.plot_all_LST(vImg,vLST,vtimestamp)


# 

# In[22]:


def plot_islands(original,lst,detected_island,limit=None,enhance_radius=False):
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



vdesired = vLST[2]
vOriginal = vImg[2]
vgray = rgb2gray(vdesired)
vgray = scale(vgray,axis=0, with_mean=True, copy=True)


# In[36]:


#plt.rcParams['figure.figsize'] = (30,30)


# ## Determinant of Hessian (DoH)¶

# In[37]:


blobs = blob_doh(vgray, max_sigma=9, threshold=.1)


# In[38]:


#plot_islands(vOriginal,vdesired,blobs)


# ### Using Threshold on the basis avg temperature of a patch

# In[39]:


'''
taking a patch of 30x30 pixel for each possible blob 
and seeing if the average temperasture is greater than 90th percentile of the temperature
''' 
vfinal= []
vrange=10
vper = np.percentile(vdesired,q=98)
for blob in blobs:
    y,x,r = blob
    y,x = y.astype(np.int64),x.astype(np.int64)
#     vmean = vdesired[x-vrange:x+vrange,y-vrange:y+vrange].mean()
    vmean = vdesired[y-vrange:y+vrange,x-vrange:x+vrange].mean()
    if vmean>vper:
        vfinal.append(np.array([y,x,r]))
vfinal = np.array(vfinal)


# In[40]:


#plot_islands(vOriginal,vdesired,vfinal,enhance_radius=True)


# In[41]:


vfinal.shape


# In[42]:


import cv2


# In[43]:

sift = cv2.xfeatures2d.SIFT_create()

#sift = cv2.SIFT()


# In[ ]:

def dtype_change(data):    
    data = (data - np.min(data)) * 255 / np.max(data)
    data = data.astype(np.uint8)
    return data

#kp1, des1 = sift.detectAndCompute(vOriginal,None)
vRange = 20
#img1 = dtype_change(rgb2gray(vFilter))
#img2 = dtype_change(rgb2gray(vOriginal))

img2 = rgb2gray(vOriginal)
img1 = img2[int(vfinal[0][0])-vRange:int(vfinal[0][0])+vRange,
                    int(vfinal[0][1])-vRange:int(vfinal[0][1]+vRange)]
img1 = dtype_change(img1)
img2 = dtype_change(img2)
# 0 and 2
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)



FLANN_INDEX_KDTREE = 0
MIN_MATCH_COUNT = 10
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1,des2,k=2)

# store all the good matches as per Lowe's ratio test.
good = []
for m,n in matches:
    if m.distance < 0.9*n.distance:
        good.append(m)
if len(good)>MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    h,w = img1.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

else:
#    print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
    matchesMask = None

draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)

img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)

plt.imshow(img3, 'gray'),plt.show()
pdb.set_trace()
