import numpy as np
from scipy.io import wavfile
import librosa

class DataProcessing():
    
    def __init__(self,file,mode):
        self.load_audio_data(file,mode)
        self.hpss_execute()
        self.chroma_execute('cqt_cens')

    def load_audio_data(self,file,mode):
        if mode=='a':
            sr,loaded_data=wavfile.read(file)
            self.sr=sr
            self.loaded_data=loaded_data.astype(np.float)

    def hpss_execute(self):
        left_h,left_p=librosa.effects.hpss(self.loaded_data[:,0])
        right_h,right_p=librosa.effects.hpss(self.loaded_data[:,1])

        self.harmonics=np.stack([left_h,right_h],1)
        self.percussive=np.stack([left_p,right_p],1)



    def chroma_execute(self,mode):
        N_BINS=48
        HOP_LENGTH=4096
        FMIN=130.813
        WIN_LEN_SMOOTH=20

        if mode=='cqt_cens':
            C_left=librosa.cqt(self.harmonics[:,0],n_bins=N_BINS,hop_length=HOP_LENGTH,fmin=FMIN)
            C_right=librosa.cqt(self.harmonics[:,1],n_bins=N_BINS,hop_length=HOP_LENGTH,fmin=FMIN)
            left_chroma_cens=librosa.feature.chroma_cens(C=C_left,hop_length=HOP_LENGTH,fmin=FMIN,win_len_smooth=WIN_LEN_SMOOTH)
            rihgt_chroma_cens=librosa.feature.chroma_cens(C=C_right,hop_length=HOP_LENGTH,fmin=FMIN,win_len_smooth=WIN_LEN_SMOOTH)

            self.chroma=np.stack([left_chroma_cens,rihgt_chroma_cens],0)