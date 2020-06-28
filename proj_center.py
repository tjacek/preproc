import numpy as np,cv2
import proj,imgs,pclouds,tools

class CenterProj(object):
    def __init__(self,dim,kern_size=(3,3)):
        self.basic_proj=proj.BasicProj(dim,kern_size)

    def __call__(self,frames):
        frames=[ proj.nonzero_points(frame_i) 
                    for frame_i in frames]
        pclouds=center(frames) 
        new_frames=self.basic_proj(pclouds)
        return new_frames

def center_pcloud(frames):
    frames=[ proj.nonzero_points(frame_i) 
                    for frame_i in frames]
    pclouds=center(frames)
    return pclouds

def imgs_only(in_path,out_path):
    fun=imgs.Pipeline([center_pcloud,pclouds.to_img])
    imgs.transform(in_path,out_path,fun)

def full_proj(seqs,out_path,kern_size=(3,3)):
    def proj_factory(i):
        funcs=[tools.median_smooth,CenterProj(i,kern_size),proj.scale]
        return imgs.Pipeline(funcs)
    proj_funcs=[proj_factory(i) for i in range(3)]
    proj.proj_template(seqs,out_path,proj_funcs)

def center(frames):
    center=pclouds.center_of_mass(frames)
    frames=[(pcloud_i.T-center.T).T for pcloud_i in frames]
    return center_norm(frames) 

def center_norm(frames):
    points=np.concatenate(frames,axis=1)
    seq_max=np.amax(np.abs(points),axis=1)
    frames=[ 64.0*((pcloud_i.T/seq_max.T).T+1.0).T 
                    for pcloud_i in frames]
    return frames
#def gauss_smooth(img_i):
#    if(type(img_i)==list):
#        return [gauss_smooth(img_j)  for img_j in img_i]
#    return cv2.GaussianBlur(img_i, (9, 9), 0)

if __name__=='__main__':
    imgs_only("../MHAD/box","../MHAD/center")