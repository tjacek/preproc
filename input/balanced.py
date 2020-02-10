import numpy as np
import imgs
import pclouds

def box_frame(in_path,out_path):
    fun=[balanced_frames]
    imgs.transform(in_path,out_path,fun,single_frame=False)


def balanced_frames(frames):
    pc_frames=pclouds.get_pclouds(frames)
    center=pclouds.center_of_mass(pc_frames)
    pc_frames=pclouds.change_cord(pc_frames,center)
    extr= (-1.0*get_extr(pc_frames))
    pc_frames=pclouds.change_cord(pc_frames,extr)
    pc_frames=rescale(pc_frames)  
    frames=[pclouds.to_img(pcloud_i)  for pcloud_i in pc_frames]
    return frames

def get_extr(pc_frames):
    extr1= pclouds.get_min(pc_frames)
    extr2= pclouds.get_max(pc_frames)
    extr=np.abs(np.array([extr1,extr2]))
    return np.amax(extr,axis=0)

def rescale(pc_frames,scale=128):
    pc_max= pclouds.get_max(pc_frames)
    pc_frames=[ (pcloud_i.T/pc_max).T for pcloud_i in pc_frames]
    pc_frames=[ (pcloud_i.T*scale).T for pcloud_i in pc_frames]
    return pc_frames
#    pc_max= pclouds.get_max(pc_frames)
#    raise Exception(pc_max)