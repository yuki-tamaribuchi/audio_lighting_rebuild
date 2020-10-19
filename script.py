from DataProcessing import DataProcessing
from Lighting import Lighting

file = 'piano_only_bpm100_original.wav'
mode = 'a'

lt=Lighting('192.168.11.99')
dp = DataProcessing(file,mode)