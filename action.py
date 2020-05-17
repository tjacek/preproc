import numpy as np
import imgs,proj

def full_proj(in_path,out_path,dim=2):  
    def helper(frames):
        frames=frame_proj(frames,dim)
        frames=np.array(frames,dtype=float)
        frames=proj.diff_img(frames)
        action_img=np.sum(frames,axis=2)
        return action_img
    transform=[helper,proj.scale]    
    imgs.action_img(in_path,out_path,transform)

def frame_proj(frames,dim):
    pclouds=[ proj.nonzero_points(frame_i) for frame_i in frames]
    pclouds=proj.normalize(pclouds)
    return [proj.get_proj(pcloud_i,dim) for pcloud_i in pclouds]


full_proj("../MSR/box","../MSR_full/xz")
#print( np.array(list(seqs.values())[0]).shape )
