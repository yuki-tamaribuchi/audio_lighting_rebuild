from phue import Bridge
import time
from multiprocessing import Process
from threading import Thread

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

    '''
    def color(self):

        def left():

            for xy in self.color_data[:,0,:]:
                start=time.time()
                cmd={
                    'xy':(xy[0],xy[1]),
                    'transitiontime':0
                }
                Thread(target=self.b.set_light,args=(self.left_lights,cmd)).start()
                end=time.time()
                time.sleep(self.color_interval-(end-start))

        def right():
            for xy in self.color_data[:,1,:]:
                start=time.time()
                cmd={
                    'xy':(xy[0],xy[1]),
                    'transitiontime':0
                }
                Thread(target=self.b.set_light,args=(self.right_lights,cmd)).start()
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
                Thread(target=self.b.set_light,args=(self.left_lights,cmd)).start()
                end=time.time()
                time.sleep(self.brightness_interval-(end-start))

        def right():
            for bri in self.brightness_data[:,1]:
                start=time.time()
                cmd={
                    'bri':int(bri*255),
                    'transitiontime':0
                }
                Thread(target=self.b.set_light,args=(self.right_lights,cmd)).start()
                end=time.time()
                time.sleep(self.brightness_interval-(end-start))

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
    '''


    def left(self):
        def color():
            for xy in self.color_data[:,0,:]:
                start=time.time()
                cmd={
                    'xy':(xy[0],xy[1]),
                    'transitiontime':0
                }
                Thread(target=self.b.set_light,args=(self.left_lights,cmd)).start()
                end=time.time()
                time.sleep(self.color_interval-(end-start))

        def brightness():
            for bri in self.brightness_data[:,0]:
                start=time.time() 
                cmd={
                    'bri':int(bri*255),
                    'transitiontime':0
                }
                Thread(target=self.b.set_light,args=(self.left_lights,cmd)).start()
                end=time.time()
                time.sleep(self.brightness_interval-(end-start))

        Thread(target=color).start()
        Thread(target=brightness).start()
        
        

    def right(self):
        def color():
            for xy in self.color_data[:,1,:]:
                start=time.time()
                cmd={
                    'xy':(xy[0],xy[1]),
                    'transitiontime':0
                }
                Thread(target=self.b.set_light,args=(self.right_lights,cmd)).start()
                end=time.time()
                time.sleep(self.color_interval-(end-start))

        def brightness():
            for bri in self.brightness_data[:,1]:
                start=time.time()
                cmd={
                    'bri':int(bri*255),
                    'transitiontime':0
                }
                Thread(target=self.b.set_light,args=(self.right_lights,cmd)).start()
                end=time.time()
                time.sleep(self.brightness_interval-(end-start))


        Thread(target=color).start()
        Thread(target=brightness).start()

    def execute(self):
        Process(target=self.left).start()
        Process(target=self.right).start()
