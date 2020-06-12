import numpy as np
import imgs,proj,pclouds

def gap_agum(frames):
    frames=[ proj.nonzero_points(frame_i) 
                    for frame_i in frames]
#    raise Exception(frames[0][:100])
#    center=pclouds.center_of_mass(frames)
#    frames=proj.normalize(frames)
    frames=[ pclouds.to_img(frame_i) for frame_i in frames]
    return frames
#    raise Exception(center)

imgs.transform("../agum/box","test",gap_agum)