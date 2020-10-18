import numpy as np
from scipy.io import wavfile
import librosa

class DataProcessing():
    
    def __init__(self,file,mode):
        self.load_audio_data(file,mode)

    def load_audio_data(self,file,mode):
        if mode=='a':
            self.sr,self.loaded_data=wavfile.read(file)

