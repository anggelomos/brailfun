""" CLI application to try the brailfun features. """

import os
os.system("sudo pigpiod")
import brailfun

braille_cell = brailfun.NewCell(power=3, time_on=1, time_off=0.5, signal_type=1)

braille_cell.init()

user_command = "_"

while user_command[0] != "e":
    user_command = input(
    """\nWrite a brailfun command
    \n[pi]nout\n[pa]rameters\n[t]rigger active_pins -> t 126\n[w]riter word -> w hola\n[g]enerator\n[rl]random_letter\n[rp]random_pattern\n[e]xit\n\nCommand: """)

    user_command = user_command.split()

    if user_command[0] == "pi":
        gpio_pins = [4, 5, 6, 12, 13, 16, 17, 18, 22, 23, 24, 26, 27]
        new_pinout = braille_cell.pinout()
        print(f"Input the bcm pin value, remember it has to be a gpio pin ({gpio_pins})\nIf you don't want to change the pin value write an *\n")

        for pin_name in new_pinout.keys():
            new_pin = 0
            while new_pin not in gpio_pins:
                new_pin = input(f"{pin_name}: ")
                if new_pin == "*":
                    break
                
                new_pin = int(new_pin)
                if new_pin in gpio_pins:
                    new_pinout[pin_name] = new_pin

        braille_cell.pinout(new_pinout["signal_pin"], new_pinout["d1"], new_pinout["d2"], new_pinout["d3"], new_pinout["d4"], new_pinout["d5"], new_pinout["d6"])

    


braille_cell.close()
os.system('sudo killall pigpiod')