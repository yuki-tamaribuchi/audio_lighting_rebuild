import numpy as np
from scipy.io import wavfile
from scipy.signal import resample
import librosa
import logging
from moviepy.video.io.VideoFileClip import VideoFileClip

formatter='%(levelname)s: %(asctime)s : %(message)s'
logging.basicConfig(level=logging.INFO,format=formatter)

class DataProcessing():
    
    def __init__(self,file,mode):
        self.load_audio_data(file,mode)
        self.hpss_execute()
        self.chroma_execute('cqt_cens')
        self.create_color_data()
        self.create_brightness_data()

    def load_audio_data(self,file,mode):
        logging.info('%s','Start Loading Data')
        if mode=='a':
            logging.info('%s','Loading Audio File')
            sr,loaded_data=wavfile.read(file)
            self.sr=sr
            self.loaded_data=loaded_data.astype(np.float)
            self.audio_sec=len(loaded_data[:,0])/sr

        if mode=='v':
            logging.info('%s','Loading Audio File')
            video_data=VideoFileClip(file)
            audio_data=video_data.audio
            self.loaded_data=audio_data.to_soundarray()
            self.sr=44100
            #self.dump_audio_array_length()
            self.audio_sec=len(self.loaded_data[:,0])/self.sr

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
        FMIN=130.813


        if mode=='cqt_cens':
            logging.info('%s','Selected CQT CENS')

            
            resample_num=int(44032*self.audio_sec)
            left_resampled=resample(self.harmonics[:,0],resample_num)
            right_resampled=resample(self.harmonics[:,1],resample_num)

            C_left=librosa.cqt(y=left_resampled,sr=self.sr,n_bins=N_BINS,fmin=FMIN,sparsity=0.6) 
            C_right=librosa.cqt(y=right_resampled,sr=self.sr,n_bins=N_BINS,fmin=FMIN,sparsity=0.6) 
            left_chroma_cens=librosa.feature.chroma_cens(C=C_left,fmin=FMIN)
            right_chroma_cens=librosa.feature.chroma_cens(C=C_right,fmin=FMIN)

            self.chroma=np.stack([left_chroma_cens,right_chroma_cens],0)



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
            [184,115,51],

            #No sound,無音,White
            [0,0,0]
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
        '''
        left_rgb=chroma_rgb[self.chroma[0,:,:].real.argmax(axis=0)]
        right_rgb=chroma_rgb[self.chroma[1,:,:].real.argmax(axis=0)]
        left_xy=np.nan_to_num(np.apply_along_axis(convert_rgb_to_xy,1,left_rgb))
        right_xy=np.nan_to_num(np.apply_along_axis(convert_rgb_to_xy,1,right_rgb))
        self.xy=np.stack([left_xy,right_xy],1)
        '''        
        
        '''
        resample_num=int(44032*self.audio_sec)
        left_resampled=resample(self.chroma[0,:,:],resample_num,axis=1)
        right_resampled=resample(self.chroma[1,:,:],resample_num,axis=1)
        '''
        chroma_cens_length=self.chroma.shape[2]
        mean_block_num=int(86/5)
        num_splits=np.ceil(chroma_cens_length/mean_block_num)
        chroma_cens_splited_left=np.array_split(self.chroma[0,:,:],num_splits,axis=1)
        chroma_cens_splited_right=np.array_split(self.chroma[1,:,:],num_splits,axis=1)

        #chroma_argmax_left=[]
        #chroma_argmax_right=[]

        def calc_max(block):
            arr=np.array(block)
            arr_sum=np.sum(arr,axis=1)
            arr_sum=np.append(arr_sum,[0.00000000001])
            arr_max=arr_sum.argmax()
            return arr_max
        
        chroma_argmax_left=[calc_max(block) for block in chroma_cens_splited_left]
        chroma_argmax_right=[calc_max(block) for block in chroma_cens_splited_right]

        '''
        for chroma_block in chroma_cens_splited_left:
            arr=np.array(chroma_block)
            arr_sum=np.sum(arr,axis=1)
            arr_max=arr_sum.argmax()
            chroma_argmax_left.append(arr_max)

        for chroma_block in chroma_cens_splited_right:
            arr=np.array(chroma_block)
            arr_sum=np.sum(arr,axis=1)
            arr_max=arr_sum.argmax()
            chroma_argmax_right.append(arr_max)
        '''

        left_rgb=[chroma_rgb[i] for i in chroma_argmax_left]
        right_rgb=[chroma_rgb[i] for i in chroma_argmax_right]
        print(left_rgb)

        left_xy=np.nan_to_num(np.apply_along_axis(convert_rgb_to_xy,1,left_rgb))
        right_xy=np.nan_to_num(np.apply_along_axis(convert_rgb_to_xy,1,right_rgb))
        self.xy=np.stack([left_xy,right_xy],1)

        logging.info('%s','End creating Color Data')
    
        

    def create_brightness_data(self):
        logging.info('%s','Start creating brightness data')
        resample_size=int((self.audio_sec/60)*300)
        logging.info('%s','Resample size=%s'% str(resample_size))
        logging.info('%s','Seconds Per Signal=%s'% str(self.audio_sec/resample_size))
        left_rs=resample(np.absolute(self.percussive[:,0]),resample_size)
        right_rs=resample(np.absolute(self.percussive[:,1]),resample_size)

        left_mean=left_rs.mean()
        right_mean=right_rs.mean()
        left_std=left_rs.std()
        right_std=right_rs.std()
        left_threshold=left_mean+(2*left_std)
        right_threshold=right_mean+(2*right_std)

        left_bri=[1.0 if 1.0<i/left_threshold else 0.0 if i<0.0 else i/left_threshold for i in left_rs]
        right_bri=[1.0 if 1.0<i/right_threshold else 0.0 if i<0.0 else i/right_threshold for i in right_rs]
        self. brightness=np.stack([left_bri,right_bri],1)
        logging.info('%s','End creating brightness data')
