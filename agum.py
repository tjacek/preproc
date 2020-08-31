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

def agum_action(frame_path,out_path):
    actions=imgs.read_frames(frame_path,True)
    agum_actions={}
    for name_i,action_i in actions.items():
        new_name="%s_1"% name_i
        new_action= np.flip(action_i,1)
        agum_actions[new_name]=new_action
    all_actions= {**actions,**agum_actions}
    files.make_dir(out_path)
    for name_i,action_i in all_actions.items():
        out_i="%s/%s.png" %(out_path,name_i)
        print(out_i)
        cv2.imwrite(out_i,action_i)

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
    
agum_action("../exp2/frames","../exp2/agum/frames")