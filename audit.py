import numpy as np
import os,os.path
import imgs

class PathDict(dict):
    def __init__(self, arg=[]):
        super(PathDict, self).__init__(arg)
    
    def lengths(self):
        return [len(os.listdir(path_i)) 
    	    for path_i in self.values()]

    def read(self,name_i):
        return imgs.read_frames(self[name_i])

    def stats(self,fun):
        return fun(self.lengths())

def read_paths(in_path):
    path_dict=PathDict()
    for name_i in os.listdir(in_path):
        path_i=f"{in_path}/{name_i}"
        path_dict[name_i]=path_i
    return path_dict

def count_files(in_path):
    return len(os.listdir(in_path))

def action_shape(in_path):
    path_dict=read_paths(in_path)
    for path_i in path_dict:
        action_i=np.array(path_dict.read(path_i))
        print(action_i.shape)	

in_path='../CZU/final'
action_shape(in_path)