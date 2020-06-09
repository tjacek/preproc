import numpy as np,cv2
import imgs,proj
from scipy import ndimage

def time(in_path,out_path):
    def helper(frames):
        size=len(frames)
        return [ np.concatenate([frames[i-1],frames[i]],axis=0) 
                    for i in range(1,size)]
    transform=[proj.scale,helper]                
    imgs.transform(in_path,out_path,transform,single_frame=False)

def diff_img(in_path,out_path):
    fun=[mean_y,get_rescale(96,64)]
    imgs.action_img(in_path,out_path,fun)

def mean(frames):
    return np.mean(frames,axis=0)

def mean_y(frames):
    return np.mean(frames,axis=1)

def diff(frames):
    return [ np.abs(frames[i] -frames[i-1])
                for i in range(1,len(frames))]

def get_rescale(dim_x,dim_y):
    def rescale(img_i):
        return cv2.resize(img_i,(dim_x,dim_y), interpolation = cv2.INTER_CUBIC)
    return rescale

def median_smooth(img_i):
    if(type(img_i)==list):
        return [median_smooth(frame_i) for frame_i in img_i]
    return ndimage.median_filter(img_i ,7)