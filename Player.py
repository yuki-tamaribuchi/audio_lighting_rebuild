import vlc
import time

class Player():
    
    def __init__(self,file,data_instance,light_instance):
        self.p=vlc.MediaPlayer()
        self.p.set_mrl(file)
        self.audio_sec=data_instance.audio_sec
        self.light_instance=light_instance

    def play(self):
        self.light_instance.execute()
        self.p.play()
        time.sleep(self.audio_sec)