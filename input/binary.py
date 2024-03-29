import numpy as np
import scipy.io
import cv2
import files
#from preproc.binary import standarize 
import h5py


def convert_inert(in_path,out_path):
    paths=files.top_files(in_path)
    files.make_dir(out_path)
    for path_i in paths:
        out_i= out_path +'/' +path_i.split('/')[-1]
        mat_i = scipy.io.loadmat(path_i)
        mat_i=mat_i['d_iner']
        np.savetxt(out_i,mat_i,delimiter=',')

def convert(in_path,out_path):
    mat_i = scipy.io.loadmat(in_path)
    seq_i=mat_i['depth']
    files.make_dir(out_path)
    print(out_path)
    for j,frame_j in enumerate(seq_i):
        name_j=f"{out_path}/{j}.png"
        cv2.imwrite(name_j,frame_j)

#def convert(in_path,out_path):
#    paths=files.top_files(in_path)
#    files.make_dir(out_path)
#    for path_i in paths:
#        print(path_i)
#        out_i= out_path +'/' +path_i.split('/')[-1]
#        files.make_dir(out_i)
#        mat_i = scipy.io.loadmat(path_i)
#        seq_i=mat_i['d_depth']
#        max_z=np.amax(seq_i)
#        for j,frame_j in enumerate(seq_i.T):
#            frame_name_j=out_i+'/'+str(j)+".png"
#            frame_j= (frame_j/max_z)*192.0 
#            cv2.imwrite(frame_name_j,frame_j.T)

def h5_convert(in_path,out_path):
    paths=files.top_files(in_path)
    files.make_dir(out_path)
    for path_i in paths:
        print(path_i)
        data_i=get_data(path_i)
        out_i="%s/%s" % (out_path,path_i.split("/")[-1])
        files.make_dir(out_i)
        for j,frame_j in enumerate(data_i):
            out_ij="%s/frame%d.png" %(out_i,j)
            cv2.imwrite(out_ij,frame_j)

def get_data(path_i):
    f_i=h5py.File(path_i, 'r')
    for k, v in f_i.items():
        return v.value