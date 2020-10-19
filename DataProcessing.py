import numpy as np
from scipy.io import wavfile
import librosa
import logging

formatter='%(levelname)s: %(asctime)s : %(message)s'
logging.basicConfig(level=logging.INFO,format=formatter)

class DataProcessing():
    
    def __init__(self,file,mode):
        self.load_audio_data(file,mode)
        self.hpss_execute()
        self.chroma_execute('cqt_cens')
        self.create_color_data()

    def load_audio_data(self,file,mode):
        logging.info('%s','Start Loading Data')
        if mode=='a':
            logging.info('%s','Loading Audio File')
            sr,loaded_data=wavfile.read(file)
            self.sr=sr
            self.loaded_data=loaded_data.astype(np.float)

        logging.info('%s','End Loading Data')

    def hpss_execute(self):
        logging.info('%s','Start HPSS')
        left_h,left_p=librosa.effects.hpss(self.loaded_data[:,0])
        right_h,right_p=librosa.effects.hpss(self.loaded_data[:,1])

        self.harmonics=np.stack([left_h,right_h],1)
        self.percussive=np.stack([left_p,right_p],1)

        logging.info('%s','End HPSS')



    def chroma_execute(self,mode):
        logging.info('%s','Start Chroma')
        N_BINS=48
        HOP_LENGTH=4096
        FMIN=130.813
        WIN_LEN_SMOOTH=20

        if mode=='cqt_cens':
            logging.info('%s','Selected CQT CENS')
            C_left=librosa.cqt(self.harmonics[:,0],n_bins=N_BINS,hop_length=HOP_LENGTH,fmin=FMIN)
            C_right=librosa.cqt(self.harmonics[:,1],n_bins=N_BINS,hop_length=HOP_LENGTH,fmin=FMIN)
            left_chroma_cens=librosa.feature.chroma_cens(C=C_left,hop_length=HOP_LENGTH,fmin=FMIN,win_len_smooth=WIN_LEN_SMOOTH)
            rihgt_chroma_cens=librosa.feature.chroma_cens(C=C_right,hop_length=HOP_LENGTH,fmin=FMIN,win_len_smooth=WIN_LEN_SMOOTH)

            self.chroma=np.stack([left_chroma_cens,rihgt_chroma_cens],0)

        logging.info('%s','End Chroma')

    def create_color_data(self):
        logging.info('%s','Start creating Color Data')

        chroma_rgb=np.array([
            #Kari Ziets' research 1931
            #Color Name to RGB Reference -> https://web.njit.edu/~walsh/rgb.html

            #C,ド,Red
            [255,0,0],

            #C#,ド#(レb),Purple
            [160,32,240],

            #D,レ,Violet
            [238,130,238],

            #D#,レ#(ミb),LightBlue
            [173,216,230],

            #E,ミ,Gold
            [255,215,0],

            #F,ファ,Pink
            [255,192,203],

            #F#,ファ#(ソb),turquoise4
            [0,134,139],

            #G,ソ,SkyBlue
            [135,206,235],

            #G#,ソ#(ラb),Unknown -> mean of G and A
            [195,230,79],

            #A,ラ,冷たい黄 -> Yellow
            [255,255,0],

            #A#,ラ#(シb),Orange
            [255,165,0],

            #B,シ,Copper
            [184,115,51]
        ])

        def convert_rgb_to_xy(data):
            r_gamma = pow( ((data[0]/256) + 0.055) / (1.0 + 0.055), 2.4 ) if (data[0]/256) > 0.04045 else ((data[0]/256) / 12.92)
            g_gamma = pow( ((data[1]/256) + 0.055) / (1.0 + 0.055), 2.4 ) if (data[1]/256) > 0.04045 else ((data[1]/256) / 12.92)
            b_gamma = pow( ((data[2]/256) + 0.055) / (1.0 + 0.055), 2.4 ) if (data[2]/256) > 0.04045 else ((data[2]/256) / 12.92)

            x = r_gamma * 0.649926 + g_gamma * 0.103455 + b_gamma * 0.197109
            y = r_gamma * 0.234327 + g_gamma * 0.743075 + b_gamma * 0.022598
            z = g_gamma * 0.053077 + b_gamma * 1.035763

            x=x/(x+y+z)
            y=y/(x+y+z)

            return x,y

        left_rgb=chroma_rgb[self.chroma[0,:,:].real.argmax(axis=0)]
        right_rgb=chroma_rgb[self.chroma[1,:,:].real.argmax(axis=0)]
        left_xy=np.nan_to_num(np.apply_along_axis(convert_rgb_to_xy,1,left_rgb))
        right_xy=np.nan_to_num(np.apply_along_axis(convert_rgb_to_xy,1,right_rgb))
        self.xy=np.stack([left_xy,right_xy],1)
        logging.info('%s','End creating Color Data')
    
        

    def create_brightness_data(self):
        pass