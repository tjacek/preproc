import os,re

class Name(str):
    def __new__(cls, p_string):
        return str.__new__(cls, p_string)

    def __len__(self):
        return len(self.split('_'))

    def clean(self):
        digits=[ str(int(digit_i)) 
                for digit_i in re.findall(r'\d+',self)]
        return Name("_".join(digits))

    def get_cat(self):
        return int(self.split('_')[0])-1

    def get_person(self):
        return int(self.split('_')[1])

    def subname(self,k):
        subname_k="_".join(self.split("_")[:k])
        return Name(subname_k)

class NameList(list):
    def __new__(cls, name_list=None):
        if(name_list is None):
            name_list=[]
        return list.__new__(cls,name_list)

    def n_cats(self):
        return len(self.unique_cats())

    def unique_cats(self):
        return set(self.get_cats())

    def get_cats(self):
        return [name_i.get_cat() for name_i in self]     

    def binarize(self,j):
        return [ int(cat_i==0) for cat_i in self.get_cats()]

    def by_cat(self):
        cat_dict={cat_j:NameList() 
                for cat_j in self.unique_cats()}
        for name_i in self:
            cat_dict[name_i.get_cat()].append(name_i)
        return cat_dict

    def cats_stats(self):
        stats_dict={ cat_i:0 for cat_i in self.unique_cats()}
        for cat_i in self.get_cats():
            stats_dict[cat_i]+=1
        return stats_dict

    def subset(self,indexes):
        return NameList([self[i] for i in indexes])

    def filtr(self,cond):
        return NameList([name_i for i,name_i in enumerate(self) 
                           if cond(i,name_i)])

    def shuffle(self):
        random.shuffle(self)
        return self

def top_files(path):
    paths=[ f"{path}/{file_i}" for file_i in os.listdir(path)]
    paths=sorted(paths,key=natural_keys)
    return paths

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]

def atoi(text):
    return int(text) if text.isdigit() else text

def make_dir(path):
    if(not os.path.isdir(path)):
        os.mkdir(path)

#def bottom_files(path,full_paths=True):
#    all_paths=[]
#    for root, directories, filenames in os.walk(path):
#        if(not directories):
#            for filename_i in filenames:
#                path_i= root+'/'+filename_i if(full_paths) else filename_i
#                all_paths.append(path_i)
#    all_paths.sort(key=natural_keys)        
#    return all_paths

#def clean_str(name_i):
#    name_i=name_i.split("/")[-1]
#    digits=[ str(int(digit_i)) for digit_i in re.findall(r'\d+',name_i)]
#    return "_".join(digits)

#def filtr(seq_dict):
#    return { name_i:seq_i 
#                for name_i,seq_i in seq_dict.items()
#                    if(person_select(name_i)) }

#def person_select(name_i):
#    name_i=clean_str(name_i)
#    return (int(name_i.split('_')[1]) % 2)==1

#def dict_of_dicts(in_path):
#    return all([ os.path.isdir(path_i)
#                for path_i in top_files(in_path)])

#def replace_path(in_path,out_path):
#    file_i=in_path.split('/')[-1]
#    return "%s/%s" % (out_path,file_i)