import numpy as np
import imgs,proj

def time(in_path,out_path):
    def helper(frames):
        size=len(frames)
        return [ np.concatenate([frames[i-1],frames[i]],axis=0) 
                    for i in range(1,size)]
    transform=[proj.scale,helper]                
    imgs.transform(in_path,out_path,transform,single_frame=False)

def sum_img(in_path,out_path):
    def sum_fun(frames):
        action_img=np.mean(frames,axis=0)
        return action_img
    imgs.action_img(in_path,out_path,sum_fun)

#sum_img("proj/Z","action/Z")
imgs.concat_seq("action/Y","action/Z","action/YZ")