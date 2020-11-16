from DataProcessing import DataProcessing
from Lighting import Lighting
from Player import Player

file = 'piano_only_bpm60_original.wav'
mode = 'a'


dp = DataProcessing(file,mode)
lt=Lighting('192.168.11.99',audio_sec=dp.audio_sec,color_data=dp.xy,brightness_data=dp.brightness,left_lights=4,right_lights=2)
player=Player(file,dp,lt)
player.execute()
