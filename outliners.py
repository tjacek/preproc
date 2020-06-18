import numpy as np
import imgs,proj#,proj_center
import pclouds

def outliner_transform(in_path,out_path):
    seqs=imgs.read_seqs(in_path)
    seqs={ name_i:outliner(seq_i) 
            for name_i,seq_i in seqs.items()}
    imgs.save_seqs(seqs,out_path)

def outliner(frames):
    frames=[ proj.nonzero_points(frame_i) 
                    for frame_i in frames]
    center=pclouds.center_of_mass(frames)
    frames=[(pcloud_i.T-center.T).T for pcloud_i in frames]
    seq_min=proj.get_min(frames)
    seq_max=proj.get_max(frames)
    def helper(points):
#        neg=points[:,np.where(points[1,:]<0)]
#        neg=np.squeeze(neg)
#        pos=points[:,np.where(points[1,:]>0)]
#        pos=np.squeeze(neg)

#        points=np.concatenate([pos,neg],axis=1)
#        raise Exception(points.shape)
        points=np.array(proj.normalize(points))
        return pclouds.to_img(points)
    return [ helper(points) for points in frames]

outliner_transform("../agum/box","test")