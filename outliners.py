import numpy as np
import imgs,proj#,proj_center
import pclouds

def outliner_transform(in_path,out_path):
    seqs=imgs.read_seqs(in_path)
    seqs={ name_i:outliner(seq_i) 
            for name_i,seq_i in seqs.items()}
    imgs.save_seqs(seqs,out_path)

def outliner(frames):
    print(len(frames))
    frames=[ proj.nonzero_points(frame_i) 
                    for frame_i in frames]
    center=pclouds.center_of_mass(frames)
    frames=[(pcloud_i.T-center.T).T for pcloud_i in frames]
    seq_min=proj.get_min(frames)
    seq_max=proj.get_max(frames)
    max_y,min_y=seq_max[1],seq_min[1]
    def helper(points):
        neg=points[:,np.where(points[1,:]<0)]
        pos=points[:,np.where(points[1,:]>=0)]
        pos=square_scale(pos,max_y)
        neg=np.squeeze(neg)
        points=np.concatenate([pos,neg],axis=1)
#        raise Exception(np.amax(points,axis=1))
#        points=np.squeeze(points)
        points=np.array(proj.normalize(points))
        return pclouds.to_img(points)
    return [ helper(points) for points in frames]

def square_scale(points,const):
    y=points[1,:]
    y/=const
    y=y**2
    y*=const
#    y/= (const**2)
    arrays=[points[0,:],y,points[2,:]]
    new_points=np.concatenate(arrays,axis=0)
    return new_points 

outliner_transform("../agum/box","test")