import numpy as np

def nonzero_points(frame_i):
    xy_nonzero=np.nonzero(frame_i)
    z_nozero=frame_i[xy_nonzero]
    xy_nonzero,z_nozero=np.array(xy_nonzero),z_nozero
    x= xy_nonzero[0] / frame_i.shape[0]
    y= xy_nonzero[1] / frame_i.shape[1]
    return np.array([x,y,z_nozero])

def center_of_mass(pclouds):
    all_points=[]
    for pcloud_i in pclouds:
        for point_j in pcloud_i.T:
            all_points.append(point_j)
    return np.mean(all_points,axis=0)