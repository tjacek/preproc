import cv2

class ScaleAgum(object):
	def __init__(self,delta_x,delta_y):
        self.delta_x=delta_x
        self.delta_y=delta_y

    def __call__(self,frames):
        old_x,old_y=frames[0].shape
        new_x=int(self.delta_x*old_x)
        new_y=int(self.delta_y*old_y)
        return [cv2.resize(frame_i,(dim_x,dim_y), interpolation = cv2.INTER_CUBIC)
                    for frame_i in frames]
