import numpy as np

def get_pclouds(frames):
    return [ nonzero_points(frame_i) for frame_i in frames]

def nonzero_points(frame_i):
    xy_nonzero=np.nonzero(frame_i)
    z_nozero=frame_i[xy_nonzero]
    xy_nonzero,z_nozero=np.array(xy_nonzero),z_nozero
    x= xy_nonzero[0] #/ frame_i.shape[0]
    y= xy_nonzero[1] #/ frame_i.shape[1]
    return np.array([x,y,z_nozero])

def center_of_mass(pclouds):
    all_points=[]
    for pcloud_i in pclouds:
        for point_j in pcloud_i.T:
            all_points.append(point_j)
    return np.mean(all_points,axis=0)

def change_cord(pclouds,center):
    return [ (pcloud_i.T-center).T for pcloud_i in pclouds]

def get_max(pclouds):
    return np.amax([ np.amax(pcloud_i,axis=1) 
                      for pcloud_i in pclouds],axis=0)

def get_min(pclouds):
    return np.amin([ np.amin(pcloud_i,axis=1) 
                      for pcloud_i in pclouds],axis=0)

def to_img(pcloud,scale=128):
    img_i=np.zeros((scale,scale))
    for point_j in pcloud.T:
        x_j,y_j=int(point_j[0]),int(point_j[1])
        if( x_j<scale  and y_j<scale):
            img_i[x_j][y_j]=point_j[2]
    return img_i