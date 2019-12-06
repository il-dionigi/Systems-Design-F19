import time
import board
import neopixel
import math

def horizontal_scroll(iter,coords,max_dim):
	gradient = math.ceil(255/(max_dim[0]-1))


