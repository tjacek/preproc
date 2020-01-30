import numpy as np
import imgs,proj

def time(in_path,out_path):
    def helper(frames):
        size=len(frames)
        return [ np.concatenate([frames[i-1],frames[i]],axis=0) 
                    for i in range(1,size)]
    transform=[helper,proj.scale]                
    imgs.transform(in_path,out_path,transform,single_frame=False)

time("../MSR/box","../MSR/time")