import imgs

in_path="../box"
img_dict=imgs.read_seqs(in_path)
for seq_i in img_dict.values():
    print(seq_i[0].shape)	