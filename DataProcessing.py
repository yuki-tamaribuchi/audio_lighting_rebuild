import numpy as np
from scipy.io import wavfile
import librosa

class DataProcessing():
    
    def __init__(self,file,mode):
        self.load_audio_data(file,mode)

    def load_audio_data(self,file,mode):
        if mode=='a':
            self.sr,self.loaded_data=wavfile.read(file)

    def hpss_execute(self):
        self.left_harmonics,self.left_percussive=librosa.effects.hpss(self.loaded_data[:,0])
        self.right_harmonics,self.right_percussive=librosa.effects.hpss(self.loaded_data[:,1])

    def chroma_execute(self,mode):
        N_BINS=48
        HOP_LENGTH=4096
        FMIN=130.813
        WIN_LEN_SMOOTH=20


        if mode=='cqt':
            C_left=librosa.cqt(self.left_harmonics,n_bins=N_BINS,hop_length=HOP_LENGTH,fmin=FMIN)
            C_right=librosa.cqt(self.right_harmonics,n_bins=N_BINS,hop_length=HOP_LENGTH,fmin=FMIN)
            self.left_cens=librosa.feature.chroma_cens(C_left,hop_length=HOP_LENGTH,fmin=FMIN,win_len_smooth=WIN_LEN_SMOOTH)
            self.rihgt_cens=librosa.feature.chroma_cens(C_right,hop_length=HOP_LENGTH,fmin=FMIN,win_len_smooth=WIN_LEN_SMOOTH)
