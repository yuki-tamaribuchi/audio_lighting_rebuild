from phue import Bridge
import time
from multiprocessing import Process

class Lighting():
    def __init__(self,ip_addr,audio_sec,color_data=None,brightness_data=None,left_lights=None,right_lights=None):
        self.b=Bridge(ip_addr)
        self.b.connect()
        self.audio_sec=audio_sec
        self.color_data=color_data
        self.brightness_data=brightness_data
        self.left_lights=left_lights
        self.right_lights=right_lights
        
        self.calc()
        

    def calc(self):
        self.color_data_length=len(self.color_data[:,0])
        self.brightness_data_length=len(self.brightness_data[:,0])
        self.color_interval=self.audio_sec/self.color_data_length
        self.brightness_interval=self.audio_sec/self.brightness_data_length

    def color(self):

        def left():

            for xy in self.color_data[:,0,:]:
                start=time.time()
                cmd={
                    'xy':(xy[0],xy[1]),
                    'transitiontime':0
                }
                self.b.set_light(self.left_lights,cmd)
                end=time.time()
                time.sleep(self.color_interval-(end-start))

        def right():
            for xy in self.color_data[:,1,:]:
                start=time.time()
                cmd={
                    'xy':(xy[0],xy[1]),
                    'transitiontime':0
                }
                self.b.set_light(self.right_lights,cmd)
                end=time.time()
                time.sleep(self.color_interval-(end-start))

        processes=[
            Process(target=left),
            Process(target=right)
        ]
        for p in processes:
            p.start()

    def brightness(self):

        def left():
            for bri in self.brightness_data[:,0]:
                start=time.time() 
                cmd={
                    'bri':int(bri*255),
                    'transitiontime':0
                }
                self.b.set_light(self.left_lights,cmd)
                end=time.time()
                time.sleep(self.color_interval-(end-start))

        def right():
            for bri in self.brightness_data[:,1]:
                start=time.time()
                cmd={
                    'bri':int(bri*255),
                    'transitiontime':0
                }
                self.b.set_light(self.right_lights,cmd)
                end=time.time()
                time.sleep(self.color_interval-(end-start))

        processes=[
            Process(target=left),
            Process(target=right)
        ]
        for p in processes:
            p.start()

    def execute(self):
        processes=[
            Process(target=self.color,),
            Process(target=self.brightness,)
        ]
        for p in processes:
            p.start()