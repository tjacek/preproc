import numpy as np
from scipy.stats import skew,pearsonr
import imgs,files

def compute(in_path,out_path,upsample=False):
    seq_dict=imgs.read_seqs(in_path)
#    extract=Extractor()
    files.make_dir(out_path)
    for name_i,seq_i in seq_dict.items():
        feat_seq_i=extract(seq_i)
        name_i=name_i.split('.')[0]+'.txt'
        out_i=out_path+'/'+name_i
        np.savetxt(out_i,feat_seq_i,delimiter=',')

def extract(frames):
    pclouds=prepare_pclouds(frames)
    pclouds=outliner(pclouds)
    feats=np.array([std_feat(pcloud_i) for pcloud_i in pclouds])
    return np.array(feats)

def prepare_pclouds(frames):
    pclouds=[nonzero_points(frame_i) for frame_i in frames]
    center=center_of_mass(pclouds)
    return [(pcloud_i.T-center).T for pcloud_i in pclouds]

def nonzero_points(frame_i):
    xy_nonzero=np.nonzero(frame_i)
    z_nozero=frame_i[xy_nonzero]
    xy_nonzero,z_nozero=np.array(xy_nonzero),z_nozero#np.expand_dims(z_nozero,axis=0)
    x= xy_nonzero[0] / frame_i.shape[0]
    y= xy_nonzero[1] / frame_i.shape[1]
    return np.array([x,y,z_nozero])

def center_of_mass(pclouds):
    all_points=[]
    for pcloud_i in pclouds:
        for point_j in pcloud_i.T:
            all_points.append(point_j)
    return np.mean(all_points,axis=0)

def outliner(pclouds):
    return [ pcloud_i *pcloud_i*np.sign(pcloud_i) for pcloud_i in pclouds ]

#def area(frame_i):
#    return [np.count_nonzero(frame_i)/np.prod(frame_i.shape)]

def max_z(points):
    max_index=np.argmax(points[2])
    extr=points[:,max_index]
    return [extr[0],extr[1]]

def std_feat(points):
    return list(np.std(points,axis=1))

def skew_feat(points):
#    std_i=list(np.std(points,axis=1))
    skew_i=list(skew(points,axis=1))
    return skew_i

def corl(points):
    x,y,z=points[0],points[1],points[2]
    return [pearsonr(x,y)[0],pearsonr(z,y)[0],pearsonr(x,z)[0]]


compute("../MSR_att/box","std")
