import cv2
import agum,imgs,files

def get_action_agum():
    return agum.AgumTemplate([agum.flip_agum],action_read,action_save)

def action_read(in_path):
    return imgs.read_frames(in_path,True)

def action_save(all_samples,out_path):
    files.make_dir(out_path)
    for name_i,action_i in all_samples.items():
        out_i="%s/%s.png" %(out_path,name_i)
        print(out_i)
        cv2.imwrite(out_i,action_i)