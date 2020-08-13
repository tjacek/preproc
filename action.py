import numpy as np
import imgs,proj,outliners,tools

class BuildActionImg(object):
    def __init__(self,funcs):
        self.funcs=funcs
        self.scale=proj.Scale()

    def __call__(self,frames):
        sub_imgs=[func_i(frames) for func_i in self.funcs]
        sub_imgs=[self.scale(img_i) for img_i in sub_imgs]
        return np.concatenate(sub_imgs,axis=0)

def many_action_img(in_path,out_path):
#    def helper(frames):
#        img0=simple_proj(frames)
#        img1=time_max(frames)
#        return np.concatenate([img0,img1],axis=0)
#    funcs=[helper,proj.Scale()]
    helper=BuildActionImg([time_max])
    imgs.action_img(in_path,out_path,helper)

#def single_action_img(in_path,out_path):
#    funcs=[static_max,proj.Scale()]
#    imgs.action_img(in_path,out_path,funcs)

def medium_reg(frames):
    i= int(len(frames)/2)
    return frames[i]

def simple_proj(frames):
    frames=np.array(frames)
    frames[frames!=0]=1.0
    return np.sum(frames,axis=0)

def static_max(frames):
    frames=np.array([z_spot(1.0,img_i) for i,img_i in enumerate(frames)
                               if(not img_i is None)])
    action_i=np.sum(frames,axis=0)
    print(action_i.shape)
    action_i[action_i!=0]=100.0
    return action_i

def time_max(frames):
    frames=np.array([z_spot(i,img_i) for i,img_i in enumerate(frames)
                               if(not img_i is None)])
    action_i=np.mean(frames,axis=0)
    print(action_i.shape)
    action_i*=100.0
    return action_i

def z_spot(i,img_i):
    x,y=np.unravel_index(np.argmax(img_i),img_i.shape)
#    img_i=img_i.astype(float)
    img_i=np.zeros( img_i.shape,dtype=float)
    img_i[ x-5:x+5, y-5:y+5]=float(i)

    return img_i

many_action_img("../MSR_exp1/box","../MSR_exp1/exp2/frames")