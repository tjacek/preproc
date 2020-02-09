import numpy as np
from scipy.stats import skew,pearsonr
import imgs,files,pclouds

def compute(in_path,out_path,upsample=False):
    seq_dict=imgs.read_seqs(in_path)
    files.make_dir(out_path)
    for name_i,seq_i in seq_dict.items():
        feat_seq_i=extract(seq_i)
        name_i=name_i.split('.')[0]+'.txt'
        out_i=out_path+'/'+name_i
        np.savetxt(out_i,feat_seq_i,delimiter=',')

def extract(frames):
    pclouds=prepare_pclouds(frames)
    pclouds=outliner(pclouds)
#    feats0=np.array([max_z(pcloud_i) for pcloud_i in pclouds])
#    feats1=np.array([skew_feat(pcloud_i) for pcloud_i in pclouds])
#    feats2=np.array([corl(pcloud_i) for pcloud_i in pclouds])
    feats3=np.array([std_feat(pcloud_i) for pcloud_i in pclouds])
#    full=np.concatenate([feats0,feats1,feats2,feats3],axis=1)
    return feats3

def prepare_pclouds(frames):
    pclouds=[pclouds.nonzero_points(frame_i) for frame_i in frames]
    center=pclouds.center_of_mass(pclouds)
    return [(pcloud_i.T-center).T for pcloud_i in pclouds]

def get_max(pclouds):
    return np.amax([ np.amax(pcloud_i,axis=1) 
                      for pcloud_i in pclouds],axis=0)

def outliner(pclouds):
    out=[ pcloud_i *pcloud_i*np.sign(pcloud_i) for pcloud_i in pclouds ]
    pc_max=get_max(out)
    pclouds=[ (pcloud_i.T/pc_max).T for pcloud_i in pclouds]
    return pclouds

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


compute("../MHAD2/box","../MHAD2/seqs/std")
