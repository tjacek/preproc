import numpy as np
import imgs

def box_frame(in_path,out_path):
    fun=[equal_box]#[extract_box]
    imgs.transform(in_path,out_path,fun,single_frame=False)

def rescale_imgs(in_path,out_path):
    imgs.transform(in_path,out_path,norm_z,single_frame=False)

def norm_z(frames,max_value=240.0):
    frames=np.array(frames).astype(float)
    min_z,max_z=np.amin(frames),np.amax(frames)
    delta_z=max_z-min_z
    zero_points=(frames==0)
    frames-=(min_z-0.01*delta_z) 
    max_z=np.amax(frames)
    frames=(frames/max_z)*max_value
    frames=np.abs(frames-max_value)
    frames[zero_points]=0.0
    return frames

def equal_box(frames):
    frames=extract_box(frames)
    def helper(img_i):
        x,y=img_i.shape
        ratio=x/y
        if(ratio<1):
            img_i=img_i.T
            x,y=y,x
        delta=x-y
        parity=delta % 2
        x_img=np.zeros((x,int(delta/2)))
        y_img=np.zeros((x,int(delta/2+parity)))
        img_i=np.concatenate([x_img,img_i,y_img],axis=1)
        if(ratio<1):
            img_i=img_i.T
        return img_i
    return [helper(frame_i) for frame_i in frames]

def extract_box(frames):
    bounds=[ frame_bounds(frame_i) for frame_i in frames]
    bound_seq=np.array([frame_i for frame_i in bounds
                            if(not frame_i is None)])
    max_values=np.amax(bound_seq[:,:2],axis=0)
    min_values=np.amin(bound_seq[:,2:],axis=0)
    print(max_values)
    print(min_values)
    (max_x,max_y),(min_x,min_y)=max_values,min_values
    def box_helper(frame_i):
        return frame_i[min_x:max_x,min_y:max_y]
    return np.array([box_helper(frame_i) for frame_i in frames])

def frame_bounds(frame_i):
    nonzero_i=np.array(np.nonzero(frame_i))
    if(nonzero_i.shape[1]==0):
        return None
    f_max=np.max(nonzero_i,axis=1)
    f_min=np.min(nonzero_i,axis=1)
    return np.concatenate([f_max,f_min])

