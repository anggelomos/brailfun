""" CLI application to try the brailfun features. """

import os
os.system("sudo pigpiod")
import brailfun

braille_cell = brailfun.NewCell(power=3, time_on=1, time_off=0.5, signal_type=1)

braille_cell.init()

braille_cell.close()
os.system('sudo killall pigpiod')