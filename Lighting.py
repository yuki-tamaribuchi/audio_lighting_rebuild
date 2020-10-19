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
            for i in range(0,self.color_data_length):
                start=time.time()

                cmd_left={
                    'xy':(self.color_data[i,0,0],self.color_data[i,0,1]),
                    'transitiontime':0,
                }
                self.b.set_light(self.left_lights,cmd_left)
                time.sleep(self.color_interval-(time.time()-start))

        def right():
            for i in range(0,self.color_data_length):
                start=time.time()
                cmd_right={
                    'xy':(self.color_data[i,1,0],self.color_data[i,1,1]),
                    'transitiontime':0,
                }
                self.b.set_light(self.right_lights,cmd_right)
                time.sleep(self.color_interval-(time.time()-start))

        processes=[
            Process(target=left),
            Process(target=right)
        ]
        for p in processes:
            p.start()

    def brightness(self):

        def left():
            for i in range(0,self.brightness_data_length):
                start=time.time() 
                cmd_left={
                    'bri':int(self.brightness_data[i,0]*255),
                    'transitiontime':0
                }
                
                self.b.set_light(self.left_lights,cmd_left)
                
                time.sleep(self.brightness_interval-(time.time()-start))

        def right():
            for i in range(0,self.brightness_interval):
                start=time.time()
                cmd_right={
                    'bri':int(self.brightness_data[i,0]*255),
                    'transitiontime':0
                }
                self.b.set_light(self.right_lights,cmd_right)
                time.sleep(self.color_interval-(time.time()-start))

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