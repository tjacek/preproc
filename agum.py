import cv2,imgs

class ScaleAgum(object):
    def __init__(self,delta_x,delta_y):
        self.delta_x=delta_x
        self.delta_y=delta_y

    def __call__(self,frames):
        old_x,old_y=frames[0].shape
        new_x=int(self.delta_x*old_x)
        new_y=int(self.delta_y*old_y)
        return [cv2.resize(frame_i,(new_x,new_y), interpolation = cv2.INTER_CUBIC)
                    for frame_i in frames]

def agum_frames(frame_path,out_path,agum):
    seqs=imgs.read_seqs(frame_path)
    agum_seqs=[]
    for name_i,seq_i in seqs.items():
        agum_seqs+=[ ("%s_%d"% (name_i,j),agum_j(seq_i)) 
                        for j,agum_j in enumerate(agum)]
        agum_seqs.append((name_i,seq_i))
    agum_seqs=dict(agum_seqs)                
    imgs.save_seqs(agum_seqs,out_path)

agum_frames("../agum/full","../agum/scale",[ScaleAgum(1.0,1.25)])