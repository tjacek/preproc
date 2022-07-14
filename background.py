import numpy as np
import cv2
import exp

#exp.frame_exp()
def bg_substr(frames):
    diff_frames=mog_sub(frames)
    frame_cc=[ccomponent(frame_i)  
        for frame_i in diff_frames]
    mean_img=np.mean(frame_cc,axis=0)
    mean_img[mean_img!=0]=150
    mean_img= mean_img.astype("uint8")
    max_cc,labels,stats=cc_raw(mean_img)
    x,y,w,h,_=stats
    return [frame_i[y:y+w,x:x+h] 
              for frame_i in frames]

#@exp.frame_exp()
def mog_sub(frames):
    print(len(frames))
    mog = cv2.createBackgroundSubtractorMOG2();
    for frame in frames:
        mog.apply(frame,(5,5))
    bg_img = mog.getBackgroundImage()	
    new_frames=[np.abs(frame_i-bg_img) for frame_i in frames]
    return new_frames

#@exp.frame_exp(single=True)
def ccomponent(img_i):
    print(img_i.shape)
    thres = cv2.threshold(img_i,100,255,cv2.THRESH_BINARY)[1]
    max_cc,labels,stats=cc_raw(thres)
    cc_i= (labels==max_cc).astype("uint8")*255
    print(cc_i.shape)
    return cc_i

def cc_raw(thres):
    output = cv2.connectedComponentsWithStats(thres,8, cv2.CV_32S)
    (numLabels, labels, stats, centroids) = output
    area = [stats[i, cv2.CC_STAT_AREA] for i in range(numLabels)]
    max_cc=np.argsort(area)[-2]
    return max_cc,labels,stats[max_cc]

in_path="../CZU-MHAD/test"
exp.frame_exp()(bg_substr)(in_path,"test2")