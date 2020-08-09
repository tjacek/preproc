import numpy as np
import imgs,proj,outliners,tools

def z_action_img(in_path,out_path):
    def helper(frames):
        frames=np.array([z_spot(img_i) for img_i in frames])
        action_i=np.sum(frames,axis=0)
        action_i[action_i!=0]=100
        return action_i
    imgs.action_img(in_path,out_path,helper)

def z_spot(img_i):
    x,y=np.unravel_index(np.argmax(img_i),img_i.shape)
    img_i.fill(0)
    img_i[ x-5:x+5, y-5:y+5]=100
    return img_i

#def single_proj(in_path,out_path,dim=0,diff=True):  
#    transform=get_transform(dim,diff)
#    imgs.action_img(in_path,out_path,transform)

#def all_proj(in_path,out_path,diff=True):
#    funcs=[get_transform(dim,diff) for dim in range(3)]
#    def helper(frames):
#        proj_imgs=[ fun_j(frames) for fun_j in funcs]
#        return np.concatenate(proj_imgs,axis=0)  
#    imgs.action_img(in_path,out_path,helper)

#def get_transform(dim=0,diff=True):
#    def helper(frames):
#        frames=np.array(frames,dtype=float)
#        if(diff):
#            frames=tools.diff(frames)
#        action_img=np.mean(frames,axis=0)
#        return action_img
#    preproc=outliners.build_proj(dim,pipe=False,resize=(96,64))
#    transform=preproc+[helper,proj.Scale()]
#    return imgs.Pipeline(transform)

z_action_img("box","test")