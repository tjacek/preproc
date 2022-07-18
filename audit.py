import numpy as np
import os,os.path

class PathDict(dict):
    def __init__(self, arg=[]):
        super(PathDict, self).__init__(arg)
    
    def lengths(self):
        return [len(os.listdir(path_i)) 
    	    for path_i in self.values()]

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

#def action_shape(in_path):
#	frames=imgs.read_frames(in_path)
#	for frame_i in frames:
#		print(frame_i.shape)	

in_path="../CZU-MHAD/CZU-MHAD/depth"
path_dict=read_paths(in_path)
print(path_dict.stats(np.mean))
#print(count_files(in_path))