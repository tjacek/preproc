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
		out_i=files.replace_path(path_i,out_path)
		txt="\n".join(lines)
		file_str = open(out_i,'w')
		file_str.write(txt)
		file_str.close()

conv_seq("../MSR_skeleton","skeleton")