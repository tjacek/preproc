import numpy as np
import imgs,proj,proj_center
import pclouds,tools

def outliner_transform(in_path,out_path):
    seqs=imgs.read_seqs(in_path)
    seqs={ name_i:outliner(seq_i) 
            for name_i,seq_i in seqs.items()}
    imgs.save_seqs(seqs,out_path)

def outliner(frames):#,as_proj=True):
    frames=[ proj.nonzero_points(frame_i) 
                    for frame_i in frames]
    center=pclouds.center_of_mass(frames)
    frames=[(pcloud_i.T-center.T).T for pcloud_i in frames]
    assert len(frames)>0
    seq_min=proj.get_min(frames)
    seq_max=proj.get_max(frames)
    max_y,min_y=seq_max[1],seq_min[1]
    def helper(points):
        neg=points[:,np.where(points[1,:]<0)]
        pos=points[:,np.where(points[1,:]>=0)]
        pos=square_scale(pos,max_y)
        neg=square_scale(neg,min_y)
        points=np.concatenate([pos,neg],axis=1)
#        points= (points.T-seq_min.T).T
        return points
    return [ helper(points) for points in frames]

def square_scale(points,const):
    y=points[1,:]
    y/=const
    y=y**2
    y*=const
    arrays=[points[0,:],y,points[2,:]]
    new_points=np.concatenate(arrays,axis=0)
    return new_points 

def outliner_img(in_path,out_path):
    fun=[tools.median_smooth,outliner,
            proj_center.center_norm,
            pclouds.to_img,
            proj.scale]
    imgs.transform(in_path,out_path,fun)

def outliner_projection(in_path,out_path,full=True):
    proj_range= range(3) if(full) else range(1,3)
    proj_funcs=[build_proj(i) for i in proj_range]
    proj.proj_template(in_path,out_path,proj_funcs)

def build_proj(dim,kern=(3,3),pipe=True):
    proj_i=[#tools.median_smooth,
                outliner,proj_center.center_norm]
    proj_i.append(proj.BasicProj(dim,kern))
    if(pipe):
        proj_i.append(proj.Scale())
        return imgs.Pipeline(proj_i)
    return proj_i

if __name__ == "__main__":
    outliner_projection("../agum/MHAD/center","../agum/MHAD/frames",True)
#    outliner_img("box","test2")