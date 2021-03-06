import numpy as np,cv2
import imgs,files,tools

class Scale(object):
    def __init__(self,dim_x=64,dim_y=64):
        self.x=dim_x
        self.y=dim_y

    def __call__(self,binary_img):
        if(type(binary_img)==list):
            return [ self(frame_i) for frame_i in binary_img]    
        dims=(self.x,self.y)
        return cv2.resize(binary_img,dsize=dims,interpolation=cv2.INTER_CUBIC)

class Proj(object):
    def __init__(self,dim,kern_size=(3,3)):
        self.basic_proj=BasicProj(dim,kern_size)

    def __call__(self,frames):
        pclouds=[ nonzero_points(frame_i) for frame_i in frames]
        pclouds=normalize(pclouds)
        new_frames=self.basic_proj(pclouds)
        return new_frames

class BasicProj(object):
    def __init__(self,dim,kern_size=(3,3)):
        self.dim=dim
        self.kern_size=kern_size
    
    def __call__(self,pclouds):
        new_frames=[get_proj(pcloud_i,self.dim) for pcloud_i in pclouds]
        new_frames=[smooth_proj(frame_i,self.kern_size) 
                        for frame_i in new_frames]       
        return new_frames


def full_proj(seqs,out_path,kern_size=(3,3)):
    def proj_factory(i):
        funcs=[tools.median_smooth,Proj(i,kern_size),Scale()]
#        funcs=[Proj(i,kern_size),scale]
        return imgs.Pipeline(funcs)
    proj_funcs=[proj_factory(i) for i in range(3)]
    proj_template(seqs,out_path,proj_funcs)

def proj_template(in_path,out_path,proj_funcs):
    files.make_dir(out_path)
    paths=files.top_files(in_path)
    for seq_path_i in paths:
        print(seq_path_i)
        seq_i=imgs.read_frames(seq_path_i,as_dict=False)
        proj_seq_i=[proj_i(seq_i) for proj_i in proj_funcs]
        new_imgs=np.concatenate(proj_seq_i,axis=1)
        out_i="%s/%s" % (out_path,seq_path_i.split("/")[-1])
        imgs.save_frames(out_i,new_imgs)
#def proj_template(seqs,out_path,proj_funcs):
#    if(type(seqs)==str):
#        seqs=imgs.read_seqs(seqs)
#    files.make_dir(out_path)
#    for name_j,seq_i in seqs.items():
#        print(name_j)
#        proj_seq_i=[proj_i(seq_i) for proj_i in proj_funcs]
#        new_imgs=np.concatenate(proj_seq_i,axis=1)
#        out_i="%s/%s" % (out_path,name_j)
#        imgs.save_frames(out_i,new_imgs)

def nonzero_points(frame_i):
    xy_nonzero=np.nonzero(frame_i)
    z_nozero=frame_i[xy_nonzero]
    xy_nonzero,z_nozero=np.array(xy_nonzero),z_nozero#np.expand_dims(z_nozero,axis=0)
    x= xy_nonzero[0] 
    y= xy_nonzero[1]
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
    pclouds=filter_empty(pclouds)
    pc_min=get_min(pclouds)
    pclouds=[ (pcloud_i.T-pc_min) for pcloud_i in pclouds]
    pc_max=get_max(pclouds)
    pclouds=[ (pcloud_i/pc_max)*128 for pcloud_i in pclouds]
    return pclouds

def get_min(pclouds):
#    if(not pclouds):
#        return np.Inf
#    print( [ pcloud_i.shape for pcloud_i in pclouds])
    axis=1 if(pclouds[0].shape[0]==3) else 0
    return np.amin([ np.amin(pcloud_i,axis=axis) 
                      for pcloud_i in pclouds],axis=0).T

def get_max(pclouds):
    axis=1 if(pclouds[0].shape[0]==3) else 0
    return np.amax([ np.amax(pcloud_i,axis=axis) 
                      for pcloud_i in pclouds],axis=0).T

def smooth_proj(proj_i,kern_size=(3,3)):
    if(type(proj_i)==list):
        return [smooth_proj(frame_j) for frame_j in proj_i]
    kernel2= np.ones(kern_size,np.uint8)
    proj_i = cv2.dilate(proj_i,kernel2,iterations = 1)#
    proj_i[proj_i!=0]=200.0
    return proj_i

def filter_empty(pclouds):
    return [pcloud_i for pcloud_i in pclouds
                if(pcloud_i.shape[1]!=0)]


if __name__ == "__main__":
    full_proj("../action_agum_seq/seqs","../action_agum_seq/proj")
