import numpy as np
import agum,imgs

def get_seq_agum():
    seq_read=imgs.read_seqs
    seq_save=imgs.save_seqs
    return agum.AgumTemplate(flip,seq_read,seq_save)

def flip(frames):
    return [np.flip(frame_i,1) for frame_i in frames]	
