import numpy as np
import shutil,re
import files,tools

def exp(in_path,out_path,in_dict="rank_rev"):
	out_path="%s/%s" % (out_path,in_dict)
	files.make_dir(out_path)
	raw_path="%s/raw"% out_path
	reformat(in_path,raw_path,in_dict)
	scale_path="%s/frames" % out_path
	tools.rescale_imgs(raw_path,scale_path,dim_x=80,dim_y=128)

def reformat(in_path,out_path,in_dict="rank_rev"):
	pattern="%s/%i/image2/"+in_dict
	files.make_dir(out_path)
	for i in range(1,21):
		in_i=pattern % (in_path,i)
		for in_ij in files.top_files(in_i):
			print(in_ij)		
			name_ij=in_ij.split('/')[-1]
			out_ij="%s/%d_%s" %(out_path,i,name_ij)
			print(out_ij)
			shutil.copyfile(in_ij, out_ij)

def conv_seq(in_path,out_path):
	sep=re.compile("\s+")
	files.make_dir(out_path)
	for path_i in files.top_files(in_path):
		lines=open(path_i,'r').readlines()
		lines=[ ",".join(sep.split(line_i.strip())) 
				for line_i in lines]
		seq_i=np.array([np.fromstring(line_i,sep=",",dtype=float) 
					for line_i in lines])
		seq_i= skeleton_reformat(seq_i)
		out_i=files.replace_path(path_i,out_path)
		out_i=out_i.split(".")[0]
		print(out_i)
		np.save(out_i,seq_i)

def skeleton_reformat(seq_i,n_joints=20):
	ts_len=int(seq_i.shape[0]/n_joints)
	seqs=[seq_i[(i*ts_len):((i+1)*ts_len),:] 
	    	for i in range(n_joints)]
	seqs=np.concatenate(seqs,axis=1)
	return seqs

conv_seq("../MSR_skeleton","skeleton")