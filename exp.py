import os.path
import proj_center,files,imgs

def gen_proj(in_path):
    dir_path=os.path.split(in_path)[0]
    proj_path=dir_path+"/proj"
    files.make_dir(proj_path)
    names=["xy","zy","xz"]
    names=[ "%s/%s" % (proj_path,name_i) for name_i in names]
    for i,name_i in enumerate(names):
        proj_center.proj_transform(in_path,name_i,i)
    tmp_path="%s/%s" % (proj_path,"tmp")   
    imgs.concat_seq(names[1],names[2],tmp_path)
    full_path="%s/%s" % (proj_path,"full")   
    imgs.concat_seq(names[0],tmp_path,full_path)

gen_proj("MHAD/box")