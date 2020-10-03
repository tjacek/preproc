import imgs

def seq_len(in_path):
	img_dict=imgs.read_seqs(in_path)
	for seq_i in img_dict.values():
		print(seq_i[0].shape)

def action_shape(in_path):
	frames=imgs.read_frames(in_path)
	for frame_i in frames:
		print(frame_i.shape)	

in_path="../msr_rank"
action_shape(in_path)