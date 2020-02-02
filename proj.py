import numpy as np,cv2
import imgs

def proj_transform(in_path,out_path,dims=0):
    def helper(frames):
        pclouds=[ nonzero_points(frame_i) for frame_i in frames]
        pclouds=normalize(pclouds)
        new_frames=[get_proj(pcloud_i,dims) for pcloud_i in pclouds]
        new_frames=[smooth_proj(frame_i) for frame_i in new_frames]       
#        action_img=diff_img(new_frames) 
        return new_frames
    transform=[helper,scale]    
#    imgs.action_img(in_path,out_path,transform)
    imgs.transform(in_path,out_path,transform)

def nonzero_points(frame_i):
    xy_nonzero=np.nonzero(frame_i)
    z_nozero=frame_i[xy_nonzero]
    xy_nonzero,z_nozero=np.array(xy_nonzero),z_nozero#np.expand_dims(z_nozero,axis=0)
    x= xy_nonzero[0] / frame_i.shape[0]
    y= xy_nonzero[1] / frame_i.shape[1]
    return np.array([x,y,z_nozero])

def get_proj(pclouds,dims):
    img_i=np.zeros((128,128),dtype=float)
    x,y=dims,(dims+1)%3
    for point_j in pclouds:
        x_j,y_j=int(point_j[x]),int(point_j[y])
        if( x_j<128  and y_j<128):
            img_i[x_j][y_j]=200
    return img_i

def normalize(pclouds):
    pc_min=get_min(pclouds)

    pclouds=[ (pcloud_i.T-pc_min) for pcloud_i in pclouds]
    pc_max=get_max(pclouds)
    pclouds=[ (pcloud_i/pc_max)*128 for pcloud_i in pclouds]
    return pclouds

def get_min(pclouds):
    return np.amin([ np.amin(pcloud_i,axis=1) 
                      for pcloud_i in pclouds],axis=0).T

def get_max(pclouds):
    return np.amax([ np.amax(pcloud_i,axis=0) 
                      for pcloud_i in pclouds],axis=0).T

def smooth_proj(proj_i):
    if(type(proj_i)==list):
        return [smooth_proj(frame_j) for frame_j in proj_i]
    kernel2= np.ones((3,3),np.uint8)
    proj_i = cv2.dilate(proj_i,kernel2,iterations = 1)#
    proj_i[proj_i!=0]=200.0
    return proj_i

def scale(binary_img ,dim_x=64,dim_y=64):
    if(type(binary_img)==list):
        return [  scale(frame_i,dim_x,dim_y) for frame_i in binary_img]
    
    return cv2.resize(binary_img,(dim_x,dim_y), interpolation = cv2.INTER_CUBIC)

def diff_img(frames):
    return [ np.abs(frames[i] -frames[i-1])
                for i in range(1,len(frames))]

if __name__ == "__main__":
#   proj_transform("../MHAD/box","../MHAD/proj/yz",2)
    imgs.concat_seq("../MHAD/proj/tmp","../MHAD/proj/yz","../MHAD/proj/full")