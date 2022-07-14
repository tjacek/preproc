import os
import files

def rename_czu(in_path): 
    name_dict= {path_i.split('/')[-1]:path_i 
        for path_i in files.top_files(in_path)}
    cat_names=set([name_i.split("_")[0] 
    	   for name_i in name_dict])
    cat_indexes={ name_i:i
        for i,name_i in enumerate(list(cat_names))} 
    for name_i,path_i in name_dict.items():
        raw=name_i.split("_")
        out_i=f"{raw[1]}_{cat_indexes[raw[0]]}_{raw[2]}"
        os.rename(path_i,f"{in_path}/{out_i}")
        print(out_i) 

in_path="../CZU-MHAD/test"
rename_czu(in_path)