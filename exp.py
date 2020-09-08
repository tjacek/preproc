import numpy as np
import os.path
#import input.binary
import agum.seqs,agum.action,files
import input.box,tools,imgs,proj

#input.binary.h5_convert("../UWA/raw","../UWA/depth")

def action_exp(in_path,out_path,use_agum=False):
    files.make_dir(out_path)
    paths= get_paths(out_path,["action","agum"])
    def helper(frames):
        action_img=np.mean(frames,axis=0)
        return action_img#.astype('uint8')
    fun=[helper,proj.Scale()]
    imgs.action_img(in_path,paths["action"],fun)
    if(use_agum):
        agum_fun=agum.action.get_action_agum()
        agum_fun(paths["action"],paths["agum"])

def exp(in_path):
    dir_path=os.path.split(dir_path)[0]
    paths=get_paths(dir_path,["box","scale","agum"])
    input.box.box_frame(in_path,paths["box"])
    tools.rescale_imgs(paths["box"],paths["scale"],dim_x=80,dim_y=128) 
    agum_fun=agum.seqs.get_seq_agum()
    agum_fun(paths["scale"],paths["agum"])

def get_paths(dir_path,names):
    return { path_i:"%s/%s" % (dir_path,path_i) 
                for path_i in names}

action_exp("../box","../exp1",True)