import numpy as np
import os.path
#import input.binary
import imgs,proj
import input.box,tools,agum.seqs

#input.binary.h5_convert("../UWA/raw","../UWA/depth")

def action_exp(in_path,out_path):
    def helper(frames):
        action_img=np.mean(frames,axis=0)
        return action_img#.astype('uint8')
    fun=[helper,proj.Scale()]
    imgs.action_img(in_path,out_path,fun)

def exp(in_path):
    dir_path=os.path.split(in_path)[0]
    paths={ path_i:"%s/%s" % (dir_path,path_i) 
                for path_i in ["box","scale","agum"]}
    input.box.box_frame(in_path,paths["box"])
    tools.rescale_imgs(paths["box"],paths["scale"],dim_x=80,dim_y=128) 
    agum_fun=agum.seqs.get_seq_agum()
    agum_fun(paths["scale"],paths["agum"])

action_exp("../box","../exp/action")