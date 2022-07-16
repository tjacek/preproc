import numpy as np,cv2
import imgs,proj,files
from scipy import ndimage

class Rescale(object):
    def __init__(self,dims):
        self.dims=dims

    def __call__(self,img_i):
        return cv2.resize(img_i, self.dims) 

class CutImage(object):
    def __init__(self,point,dims):
        self.point=point
        self.dims=dims

    def __call__(self,img_i):
        x0,y0=self.point[0],self.point[0]+self.dims[0]
        x1,y1=self.point[1],self.point[1]+self.dims[1]
        print(type(img_i))
        return img_i[x0:y0,x1:y1] 

#def time(in_path,out_path):
#    def helper(frames):
#        size=len(frames)
#        return [ np.concatenate([frames[i-1],frames[i]],axis=0) 
#                    for i in range(1,size)]
#    transform=[proj.scale,helper]                
#    imgs.transform(in_path,out_path,transform,single_frame=False)

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

#def sigma_filtr(in_path,out_path):
#    def helper(img_i):
#        std_z= np.std(img_i)
#        value_i=np.mean(img_i)+0.5*std_z
#        print(value_i)
#        img_i[img_i< value_i]=0
#        return img_i 
#    imgs.transform(in_path,out_path,helper,True)

if __name__ == "__main__":
    in_path="../forth/frames"
    out_path="../forth/frames2"
    sigma_filtr(in_path,out_path)
#    rescale_imgs(in_path,out_path,dim_x=80,dim_y=128)