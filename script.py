from DataProcessing import DataProcessing
from Lighting import Lighting

file = 'piano_only_bpm100_original.wav'
mode = 'a'


dp = DataProcessing(file,mode)
lt=Lighting('192.168.11.99',audio_sec=dp.audio_sec,color_data=dp.xy,brightness_data=dp.brightness,left_lights=3,right_lights=1)
lt.execute()