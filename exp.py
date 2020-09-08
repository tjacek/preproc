import os.path
#import proj_center,files,imgs
#import input.binary
import input.box,tools,agum.seqs

#def gen_proj(in_path):
#    dir_path=os.path.split(in_path)[0]
#    proj_path=dir_path+"/proj"
#    files.make_dir(proj_path)
#    names=["xy","zy","xz"]
#    names=[ "%s/%s" % (proj_path,name_i) for name_i in names]
#    for i,name_i in enumerate(names):
#        proj_center.proj_transform(in_path,name_i,i)
#    tmp_path="%s/%s" % (proj_path,"tmp")   
#    imgs.concat_seq(names[1],names[2],tmp_path)
#    full_path="%s/%s" % (proj_path,"full")   
#    imgs.concat_seq(names[0],tmp_path,full_path)
#input.binary.h5_convert("../UWA/raw","../UWA/depth")

def exp(in_path):
    dir_path=os.path.split(in_path)[0]
    paths={ path_i:"%s/%s" % (dir_path,path_i) 
                for path_i in ["box","scale","agum"]}
    input.box.box_frame(in_path,paths["box"])
    tools.rescale_imgs(paths["box"],paths["scale"],dim_x=80,dim_y=128) 
    agum_fun=agum.seqs.get_seq_agum()
    agum_fun(paths["scale"],paths["agum"])

exp("../depth")