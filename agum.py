import numpy as np
import cv2,imgs,files
import proj,proj_center,gap

#class ScaleAgum(object):
#    def __init__(self,delta_x,delta_y):
#        self.delta_x=delta_x
#        self.delta_y=delta_y

#    def __call__(self,frames):
#        old_x,old_y=frames[0].shape
#        new_x=int(self.delta_x*old_x)
#        new_y=int(self.delta_y*old_y)
#        return [cv2.resize(frame_i,(new_x,new_y), interpolation = cv2.INTER_CUBIC)
#                    for frame_i in frames]

class AgumTemplate(object):
    def __init__(self, agum):
        self.agum=agum
        
    def __call__(self,in_path,out_path):
        samples=imgs.read_frames(in_path,True)
        agum_samples=[]
        for name_i,sample_i in samples.items():
            agum_samples+=[ ("%s_%d"%(name_i,j),agum_j(sample_i))
                                for j,agum_j in enumerate(self.agum)]
        all_samples= {**samples,**dict(agum_samples)}
        files.make_dir(out_path)
        for name_i,action_i in all_samples.items():
            out_i="%s/%s.png" %(out_path,name_i)
            print(out_i)
            cv2.imwrite(out_i,action_i)

def get_action_agum():
    return AgumTemplate([flip_agum])

def flip_agum(img_i):
    return np.flip(img_i,1)

def gap_agum(box_path,out_path):
    seqs=imgs.read_seqs(box_path)
    files.make_dir(out_path)
    full_path=out_path+"/full"
    train=files.filtr(seqs)
    train_gap={name_i:gap.gap_agum(seq_i) 
            for name_i,seq_i in train.items()}
    agum_path=out_path+"/agum"
    proj_center.full_proj(train_gap,agum_path,(6,6))

def simple_agum(box_path,out_path):
    seqs=imgs.read_seqs(box_path)
    files.make_dir(out_path)
    full_path=out_path+"/full"
    proj_center.full_proj(seqs,full_path,(3,3))
    train=files.filtr(seqs)
    agum_path=out_path+"/agum"
    proj_center.full_proj(train,agum_path,(6,6))
    
agum_action=get_action_agum()
agum_action("../exp2/frames","../exp2/agum/frames")