import numpy as np
import imgs,proj,pclouds

class GapTransform(object):
    def __init__(self,center,scale):
        self.center=center
        self.scale=scale

    def __call__(self,points):
        for point_i in points.T:
            if(point_i[0]>1.5*self.center[0]):
                dist=np.abs(point_i[0]-self.center[0])
                dist/=self.center[0]
                delta=dist*self.scale
                if(point_i[1]<self.center[1]):
                    point_i[1]-=delta
                else:
                    point_i[1]+=delta
        return points

def gap_agum(frames):
    frames=[ proj.nonzero_points(frame_i) 
                    for frame_i in frames]
    center=pclouds.center_of_mass(frames)
#    frames=[filtr_points(frame_i,1.5*center[0]) for frame_i in frames]
    helper=GapTransform(center,16.0)
    frames=[helper(frame_i) for frame_i in frames]
    frames=[ pclouds.to_img(frame_i) for frame_i in frames]
    return frames

def filtr_points(points,threshold):
    new_points=[]
    for point_i in points.T:
        if(point_i[0]<threshold):
            new_points.append(point_i)	
    return np.array(new_points).T

if __name__ == "__main__":
    imgs.transform("../agum/box","test",gap_agum)