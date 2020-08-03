# brailfun
Brailfun is a python module based in the pigpio library made to control a 6-dot braille cell using the gpio pins in the raspberry pi zero

Each braille cell object has these attributes and methods:

## Attributes

#### braille_pins: dict
Dictionary with the BCM pins used to control the dots in the braille cell, by default {"signal_pin":18, "d1": 4, "d2": 17, "d3": 27, "d4": 22, "d5": 23, "d6": 24}

#### power: int(1 to 5)
Integer indicating in a scall from 1 to 5 the braille cell vibration power, by default 5

#### time_on: float(0.5 to inf)
Activation signal time.

#### time_off: float(0.5 to inf)
Time between one activation signal and another one

#### signal_type: int(1 to 8)
Activation signal type, by default 1
1. Square signal
2. Triangle signal
3. Ramp signal
4. Exponential signal
5. logarithmic signal
6. Sine signal
7. Click signal (logarithmic + exponential)
8. Reverse click signal (exponential + logarithmic)

## Methods

#### init()
Initialize braille cell the pins.

#### close()
Stop pigpio session.

#### pinout(signal_pin: int, d1: int, d2: int, d3: int, d4: int, d5: int, d6: int)
Assign and initialize the braille cell bcm gpio pins.

#### parameters(power: int, time_on: float, time_off: float, signal_type: int)
Change braille cell attributes.

#### writer(text: str)
Write the text in the braille cell activating consecutively each alphanumer letter.

#### random_letter()
Write a random letter in the braille cell.

#### random_vibration()
Generate a random braille pattern and activate it in the braille cell.

## License
Whatsapp Wordcloud Generator is released under the MIT license. See LICENSE for details.

## Contact
Let's talk! Twitter/instagram: @anggelomos, email: anggelomos@outlook.com
