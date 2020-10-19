from phue import Bridge

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
        for i in self.color_data_length:
            cmd_left={
                'xy':self.color_data[i,0],
                'transitiontime':0,
            }
            cmd_right={
                'xy':self.color_data[i,1],
                'transitiontime':0,
            }
            self.b.set_light(self.left_lights,cmd_left)
            self.b.set_light(self.right_lights,cmd_right)


    def brightness(self):
        for i in self.brightness_data_length:
            cmd_left={
                'bri':self.brightness_data[i,0],
                'transitiontime':0
            }
            cmd_right={
                'bri':self.brightness_data[i,0],
                'transitiontime':0
            }
            self.b.set_light(self.left_lights,cmd_left)
            self.b.set_light(self.right_lights,cmd_right)