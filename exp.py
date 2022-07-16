import numpy as np
import cv2
import os,os.path
from functools import wraps
import files
import input.binary,imgs #import convert
#import agum.seqs,agum.action
#import input.box,tools,imgs,proj

class Pipeline(object):
    def __init__(self,transforms):
        self.transforms=transforms

    def __call__(self,frame_i):
        for transform_j in self.transforms:#[1:]:
            frame_i=transform_j(frame_i)
        return frame_i

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

def eff_frame_exp(single=False):
    def decorator(func):
        @wraps(func)
        def helper(in_path,out_path):
            files.make_dir(out_path)
            for i,path_i in enumerate(files.top_files(in_path)):
                print(f"{i}:{path_i.split('/')[-1]}")
                frames=imgs.read_frames(path_i)
                frames= func(frames)
                out_i=f"{out_path}/{path_i.split('/')[-1]}"
                imgs.save_frames(out_i,frames)
            return frames
        return helper
    return decorator

def eff_action_exp(single=False):
    def decorator(func):
        @wraps(func)
        def helper(in_path,out_path):
            files.make_dir(out_path)
            for i,path_i in enumerate(files.top_files(in_path)):
                print(f"{i}:{path_i.split('/')[-1]}")
                frames=imgs.read_frames(path_i)
                action_img= func(frames)
                out_i=f"{out_path}/{path_i.split('/')[-1]}.png"
                cv2.imwrite(out_i,action_img)
            return frames
        return helper
    return decorator

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
    in_path="../CZU-MHAD/CZU-MHAD/depth_mat"
    out_path="../CZU-MHAD/CZU-MHAD/depth"
    exp_conv=dir_funtion(input.binary.convert)
    exp_conv(in_path,out_path)
#    import tools
#    frame_exp(tools.diff)(out_path,"test")