import cv2,numpy as np#,os.path
import files

class DataDict(dict):
    def __init__(self, arg=[]):
        super(DataDict, self).__init__(arg)
    
    def names(self):
        keys=sorted(self.keys(),key=files.natural_keys) 
        return files.NameList(keys)
    
    def transform(self,fun,copy=False,single=False):
        new_dict= self.__class__() if(copy) else self
        for name_i,data_i in self.items():
            if(single):
                new_dict[name_i]=[fun(frame_j)
                    for frame_j in data_i]
            else:
                new_dict[name_i]=fun(data_i)
        return new_dict

    def save(self,out_path):
        save_seqs(self,out_path)

def read_seqs(in_path):
    seqs=DataDict()
    for seq_path_i in files.top_files(in_path):
        name_i=seq_path_i.split('/')[-1]
        seqs[name_i]=read_frames(seq_path_i)
    return seqs 

def read_frames(seq_path_i):
    return [ cv2.imread(path_j, cv2.IMREAD_GRAYSCALE)
                for path_j in files.top_files(seq_path_i)]

def save_seqs(seq_dict,out_path):
    files.make_dir(out_path)
    for name_i,seq_i in seq_dict.items():
        seq_path_i=f"{out_path}/{name_i}"
        save_frames(seq_path_i,seq_i)

def save_frames(seq_path_i,seq_i):
    files.make_dir(seq_path_i)
    for j,frame_j in enumerate(seq_i):     
        frame_name_j=f"{seq_path_i}/{j}.png" 
        cv2.imwrite(frame_name_j,frame_j)

def action_img(in_path,out_path,action_fun):
    if(type(action_fun)==list):
        action_fun=Pipeline(action_fun)
    files.make_dir(out_path)
    for in_i in files.top_files(in_path):
        frames=read_frames(in_i)
        action_img_i=action_fun(frames)
        out_i="%s/%s.png" % (out_path,in_i.split('/')[-1])
        cv2.imwrite(out_i,action_img_i)

def seq_tranform(frame_fun,img_seqs):
    if(type(frame_fun)==list):
        frame_fun=Pipeline(frame_fun)
    return { name_i:[frame_fun(frame_j) for frame_j in seq_i]
                    for name_i,seq_i in img_seqs.items()}

def concat_seq(in_path1,in_path2,out_path):
    seq1,seq2=read_seqs(in_path1),read_seqs(in_path2)
    names=seq1.keys()
    concat_seqs={}
    for name_i in names:
        seq1_i,seq2_i=seq1[name_i],seq2[name_i]
        seq_len=min(len(seq1_i),len(seq2_i))
        seq1_i,seq2_i= seq1_i[:seq_len],seq2_i[:seq_len]
        new_seq_i=np.concatenate( [seq1_i,seq2_i],axis=1)
        concat_seqs[name_i]=new_seq_i
    save_seqs(concat_seqs,out_path)

def concat_frames(in_path1,in_path2,out_path):
    seq1,seq2=read_frames(in_path1,True),read_frames(in_path2,True)
    files.make_dir(out_path)
    for name_i in seq1.keys():
        img0,img1=seq1[name_i],seq2[name_i] 
        new_img_i=np.concatenate([img0,img1],axis=0)
        cv2.imwrite(out_path+'/'+name_i+".png",new_img_i)

def transform_action_img(in_path,out_path,fun):
    files.make_dir(out_path)
    for in_i in files.top_files(in_path):
        out_i="%s/%s" % (out_path,in_i.split('/')[-1])
        img_i=cv2.imread(in_i, cv2.IMREAD_GRAYSCALE)
        new_img_i=fun(img_i)
        cv2.imwrite(out_i,new_img_i)

if __name__ == "__main__":
    in_path="../CZU-MHAD/test"
    data_dict=read_seqs(in_path)
    print(data_dict.names())