import numpy as np
import cv2
import exp

@exp.frame_exp()
def mog_sub(frames):
    print(len(frames))
    mog = cv2.createBackgroundSubtractorMOG2();
    for frame in frames:
        mog.apply(frame,(5,5))
    bg_img = mog.getBackgroundImage()	
    new_frames=[np.abs(frame_i-bg_img) for frame_i in frames]
    return new_frames

@exp.frame_exp(single=True)
def ccomponent(img_i):
    print(img_i.shape)
    return img_i	


in_path="../CZU-MHAD/test"
ccomponent(in_path,"test")