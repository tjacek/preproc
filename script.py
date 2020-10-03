import files,shutil

in_path="../Hon4d"
out_path="../msr_rank"
pattern="%s/%i/image2/rank"

files.make_dir(out_path)
for i in range(1,21):
	in_i=pattern % (in_path,i)
	for in_ij in files.top_files(in_i):
		print(in_ij)		
		name_ij=in_ij.split('/')[-1]
		out_ij="%s/%d_%s" %(out_path,i,name_ij)
		print(out_ij)
		shutil.copyfile(in_ij, out_ij)