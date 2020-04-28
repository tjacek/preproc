import numpy as np,cv2
import proj,imgs,pclouds

def proj_transform(in_path,out_path,dims=0):
    def helper(frames):
        frames=[ proj.nonzero_points(frame_i) 
                    for frame_i in frames]
  
        new_frames=[proj.get_proj(pcloud_i.T,dims) for pcloud_i in frames]
        new_frames=[proj.smooth_proj(frame_i) for frame_i in new_frames]
        return new_frames
    transform=[helper,proj.scale]    
    imgs.transform(in_path,out_path,transform)

def center(frames):
    center=pclouds.center_of_mass(frames)
    frames=[(pcloud_i.T-center.T).T for pcloud_i in frames]
    points=np.concatenate(frames,axis=1)
    seq_max=np.amax(np.abs(points),axis=1)
    frames=[ 64.0*((pcloud_i.T/seq_max.T).T+1.0) 
                    for pcloud_i in frames]
    return frames

def gauss_smooth(img_i):
    if(type(img_i)==list):
        return [gauss_smooth(img_j)  for img_j in img_i]
    return cv2.GaussianBlur(img_i, (9, 9), 0)

proj_transform("../MSR/box","testZ",2)