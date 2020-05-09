import numpy as np
import imgs,proj

def time(in_path,out_path):
    def helper(frames):
        size=len(frames)
        return [ np.concatenate([frames[i-1],frames[i]],axis=0) 
                    for i in range(1,size)]
    transform=[proj.scale,helper]                
    imgs.transform(in_path,out_path,transform,single_frame=False)

def diff_img(in_path,out_path):
    fun=[mean_y]
    imgs.action_img(in_path,out_path,fun)

def mean(frames):
    return np.mean(frames,axis=0)

def mean_y(frames):
    return np.mean(frames,axis=1)

def diff(frames):
    return [ np.abs(frames[i] -frames[i-1])
                for i in range(1,len(frames))]

diff_img("proj/X","action/X")
#imgs.concat_frames("action/X","action/YZ","action/full")