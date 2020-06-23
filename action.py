import numpy as np
import imgs,proj,outliners

def proj_img(in_path,out_path,dim=0):  
    def helper(frames):
        frames=np.array(frames,dtype=float)
        action_img=np.sum(frames,axis=0)
        return action_img
    preproc=outliners.build_proj(dim,pipe=False)
    transform=preproc+[helper,proj.scale]    
    imgs.action_img(in_path,out_path,transform)

proj_img("box","test")
#print( np.array(list(seqs.values())[0]).shape )
