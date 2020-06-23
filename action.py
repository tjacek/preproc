import numpy as np
import imgs,proj

def proj_img(in_path,out_path,dim=0):  
    frame_proj=proj.Proj(dim)
    def helper(frames):
        frames=frame_proj(frames)
        frames=np.array(frames,dtype=float)
#        frames=proj.diff_img(frames)
        action_img=np.sum(frames,axis=0)
        return action_img
    transform=[helper,proj.scale]    
    imgs.action_img(in_path,out_path,transform)

proj_img("box","test")
#print( np.array(list(seqs.values())[0]).shape )
