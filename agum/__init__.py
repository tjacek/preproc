import numpy as np
import cv2,imgs,files
import proj,proj_center,gap

class AgumTemplate(object):
    def __init__(self, agum,read,save):
        if(type(agum)!=list):
            agum=[agum]
        self.agum=agum
        self.read=read
        self.save=save
        
    def __call__(self,in_path,out_path):
        samples=self.read(in_path)
        train=files.filtr(samples)
        agum_samples=[]
        for name_i,sample_i in train.items():
            agum_samples+=[ ("%s_%d"%(name_i,j),agum_j(sample_i))
                                for j,agum_j in enumerate(self.agum)]
        all_samples= {**samples,**dict(agum_samples)}
        self.save(all_samples,out_path)

def flip_agum(img_i):
    return np.flip(img_i,1)

#def gap_agum(box_path,out_path):
#    seqs=imgs.read_seqs(box_path)
#    files.make_dir(out_path)
#    full_path=out_path+"/full"
#    train=files.filtr(seqs)
#    train_gap={name_i:gap.gap_agum(seq_i) 
#            for name_i,seq_i in train.items()}
#    agum_path=out_path+"/agum"
#    proj_center.full_proj(train_gap,agum_path,(6,6))

#def simple_agum(box_path,out_path):
#    seqs=imgs.read_seqs(box_path)
#    files.make_dir(out_path)
#    full_path=out_path+"/full"
#    proj_center.full_proj(seqs,full_path,(3,3))
#    train=files.filtr(seqs)
#    agum_path=out_path+"/agum"
#    proj_center.full_proj(train,agum_path,(6,6))