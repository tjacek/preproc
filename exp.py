import numpy as np
import os,os.path
from functools import wraps
import files
import input.binary,imgs #import convert
#import agum.seqs,agum.action
#import input.box,tools,imgs,proj

def dir_funtion(func):
    @wraps(func)
    def helper(in_path,out_path):
        files.make_dir(out_path)
        for path_i in os.listdir(in_path):
            in_i=f"{in_path}/{path_i}"
            out_i=f"{out_path}/{path_i}"
            func(in_i,out_i)
    return helper

def frame_exp(single=False):
    def decorator(func):
        @wraps(func)
        def helper(in_path,out_path):
            data_dict=imgs.read_seqs(in_path)
            data_dict.transform(func,single=single)
            data_dict.save(out_path)
            return data_dict
        return helper
    return decorator

#def action_exp(in_path,out_path,use_agum=False):
#    files.make_dir(out_path)
#    paths= get_paths(out_path,["action","agum"])
#    def helper(frames):
#        action_img=np.mean(frames,axis=0)
#        return action_img#.astype('uint8')
#    fun=[helper,proj.Scale()]
#    imgs.action_img(in_path,paths["action"],fun)
#    if(use_agum):
#        agum_fun=agum.action.get_action_agum()
#        agum_fun(paths["action"],paths["agum"])

#def exp(in_path):
#    dir_path=os.path.split(dir_path)[0]
#    paths=get_paths(dir_path,["box","scale","agum"])
#    input.box.box_frame(in_path,paths["box"])
#    tools.rescale_imgs(paths["box"],paths["scale"],dim_x=80,dim_y=128) 
#    agum_fun=agum.seqs.get_seq_agum()
#    agum_fun(paths["scale"],paths["agum"])

#def get_paths(dir_path,names):
#    return { path_i:"%s/%s" % (dir_path,path_i) 
#                for path_i in names}

if __name__ == "__main__":
    in_path="../CZU-MHAD/test_math"
    out_path="../CZU-MHAD/test"
#    exp_conv=dir_funtion(input.binary.convert)
#    exp_conv(in_path,out_path)
    import tools
    frame_exp(tools.diff)(out_path,"test")