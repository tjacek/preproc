import numpy as np,cv2
import imgs,proj,files
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

def rescale_imgs(in_path,out_path,dim_x=64,dim_y=128):
    rescale=proj.Scale(dim_x,dim_y)
    if(files.dict_of_dicts(in_path)):
        imgs.transform(in_path,out_path,rescale,True)
    else:
        imgs.transform_action_img(in_path,out_path,rescale)

def median_smooth(img_i):
    if(type(img_i)==list):
        return [median_smooth(frame_i) for frame_i in img_i]
    return ndimage.median_filter(img_i ,7)

def get_sample(seq_i):
    if(type(seq_i)==list):
        seq_i=np.array(seq_i)
    size=seq_i.shape[0]
    dist_i=get_squared_dist(size)
    def sample_helper(n):   
        return np.random.choice(np.arange(size),n,p=dist_i)
    return sample_helper

def get_squared_dist(n):
    inc,dec=np.arange(n),np.flip(np.arange(n))
    dist=np.amin(np.array([inc,dec]),axis=0)
    dist=dist.astype(float)
    dist=dist**2
    dist/=np.sum(dist)
    return dist

if __name__ == "__main__":
    in_path="../rank/raw"
    out_path="../rank/scale"
    rescale_imgs(in_path,out_path,dim_x=80,dim_y=128)