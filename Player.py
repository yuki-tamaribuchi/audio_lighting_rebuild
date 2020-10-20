import vlc
import time
from multiprocessing import Process

class Player():
    
    def __init__(self,file,data_instance,light_instance):
        self.p=vlc.MediaPlayer()
        self.p.set_mrl(file)
        self.audio_sec=data_instance.audio_sec
        self.light_instance=light_instance

    def play(self):
        self.p.play()
        time.sleep(self.audio_sec)


    def execute(self):
        processes=[
            Process(target=self.light_instance.execute),
            Process(target=self.play())
        ]
        for p in processes:
            p.start()
            p.join()