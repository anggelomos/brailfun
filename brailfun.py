import pigpio as GPIO
import math
import time
import random
from typing import Union

# This code uses BCM pins
# Tested on python 3.5.3

class new_cell:

	# The default phyisical pins are 12, 7, 11, 13, 15, 16 and 18
	# The first value is the signal BCM pin (pwm) then the next values are the vibrator BCM pins from 1 to 6
	def __init__(self, vibration_pins: dict={"signal_pin":18, "d1": 4, "d2": 17, "d3": 27, "d4": 22, "d5": 23, "d6": 24}, power: int=5, time_on: float=3, time_off: float=1, signal_type: int=1):
		self.vibration_pins = vibration_pins
		self.power = power
		self.time_on = time_on
		self.time_off = time_off
		self.signal_type = signal_type

	# GPIO setup
	pi = GPIO.pi()

	def init(self):
		"""Initialize all the pins."""
		for pin in self.vibration_pins:
			pi.set_mode(pin, GPIO.OUTPUT)
			pi.write(pin, 0)


	def pinout(self, signal_pin: int=None, d1: int=None, d2: int=None, d3: int=None, d4: int=None, d5: int=None, d6: int=None) -> dict:
		"""Assign and initialize the braille cell bcm gpio pins

		Parameters
		----------
		signal_pin : int, optional
			Signal gpio pin number (BCM), by default None
		d1-d6 : int, optional
			Braille dot gpio pin number (BCM), by default None

		Returns
		-------
		pinout: dict
			Pinout dictionary, Ex. {"signal_pin":18, "d1":4, "d2":17, "d3":27, "d4":22, "d5":23, "d6":24}
		"""
		function_arguments = locals()

		for key, value in function_arguments.items():
			if value is not None and key != "self" and isinstance(value, int):
				self.vibration_pins[key] = value

		for _, pin in self.vibration_pins.items():
			new_cell.pi.set_mode(pin, GPIO.OUTPUT)
			new_cell.pi.write(pin, 0)

		print(f"\nPinout\n{self.vibration_pins}\n")

		return self.vibration_pins
		
	@staticmethod
	def clamp(value: Union[int, float]) -> Union[int, float]:
		"""Limitate the input value between 255 and 0

		Parameters
		----------
		value : int, float
			Input value to be truncated

		Returns
		-------
		value : int, float
			A value between 0 and 255
		"""
		
		if(value>255):
			return 255
		elif(value<0):
			return 0
		else:
			return value

	@classmethod
	def close(cls):
		"""Stop pigpio session."""
		cls.pi.stop()

	def signal_square(self, dot_pattern):
		#square signal

		output=255*(self.power/5.0)
		new_cell.pi.set_PWM_dutycycle(self.vibration_pins[0], output)
			
		time.sleep(self.time_on)
		
		output=0
		new_cell.pi.set_PWM_dutycycle(self.vibration_pins[0], output)
		
		time.sleep(self.time_off)

	#señal triangular
	def s_triad(self):

		t_ini = time.time()
		
		# In this cycle the vibration signal is calculated and activated through a pwm signal
		
		while time.time() <= (t_ini + self.time_on):
			
			if time.time() < (t_ini + self.time_on/2.0):
				# First half of the cycle, t_current is calculated from 0 to time_on/2

				output = (255*(self.power/5.0))/(self.time_on/2.0)*(time.time()-t_ini)  # Here we calculate the output based on the line equation
				t_ini1 = time.time() 													# Aux variable to know the exact moment when the first cycle ends
				
			else:
		
				# Second half of the cycle, t_current is calculated from time_on/2 to time_on
				output = -(255*(self.power/5.0))/(self.time_on/2.0)*(time.time()-t_ini1)+(255*(self.power/5.0))
				
			
			output = new_cell.clamp(output)
			new_cell.pi.set_PWM_dutycycle(self.vibration_pins[0],output)
		
			
		output=0
		new_cell.pi.set_PWM_dutycycle(self.vibration_pins[0],output)
		time.sleep(self.time_off)

	#señal rampa
	def s_ramp(self):
		
		t_ini = time.time()
		
		# In this cycle the vibration signal is calculated and activated through a pwm signal
		
		while time.time() <= (t_ini + self.time_on):
		
			output = (255*(self.power/5.0))/(self.time_on)*(time.time()-t_ini)
			new_cell.pi.set_PWM_dutycycle(self.vibration_pins[0],output)
					
		output=0
		new_cell.pi.set_PWM_dutycycle(self.vibration_pins[0],output)
		time.sleep(self.time_off)

	#señal seno
	def s_sine(self):
		
		t_ini = time.time()
		
		# In this cycle the vibration signal is calculated and activated through a pwm signal
		
		while time.time() <= (t_ini + self.time_on):
			
			output = (255*(self.power/5.0))*math.sin((math.pi/self.time_on)*(time.time()-t_ini))	# In this line we calcule the half cycle of the sin function going from 0 to time_on and having a 255 in amplitude
			new_cell.pi.set_PWM_dutycycle(self.vibration_pins[0],output)
					
		output=0
		new_cell.pi.set_PWM_dutycycle(self.vibration_pins[0], output)
		time.sleep(self.time_off)

	#señal logaritmica
	def s_log(self):
		t_ini = time.time()
		
		# In this cycle the vibration signal is calculated and activated through a pwm signal
		
		while time.time() <= (t_ini + self.time_on):
			
			if time.time() < (t_ini + self.time_on/2.0):
				# First half of the cycle, t_current is calculated from 0 to time_on/2

				t_current = (2*(10-1)/(self.time_on))*(time.time() - t_ini) + 1 	# In this line we remap the time so that is goes from 1 to 10
				t_ini1 = time.time()
				
			else:
				# Second half of the cycle, t_current is calculated from time_on/2 to time_on
				
				t_current = (2*(1-10)/(self.time_on))*(time.time() - t_ini1) + 10 	# In this line we remap the time so that is goes from 10 to 1
					
					
			output = (255.0*math.log10(t_current))*(self.power/5.0)
			output = new_cell.clamp(output)
			
			
			new_cell.pi.set_PWM_dutycycle(self.vibration_pins[0],output)
			
		output=0
		new_cell.pi.set_PWM_dutycycle(self.vibration_pins[0],output)
		time.sleep(self.time_off)

	#señal exponencial
	def s_exp(self):
		
		t_ini = time.time()
		
		# In this cycle the vibration signal is calculated and activated through a pwm signal
		
		while time.time() <= (t_ini + self.time_on):
			
			if time.time() < (t_ini + self.time_on/2.0):
				# First half of the cycle, t_current is calculated from 0 to time_on/2

				t_current = (2*(math.log(10)-(-math.log(10)))/(self.time_on))*(time.time() - t_ini) + (-math.log(10)) # In this line we remap the time so that is goes from -ln(10) to ln(10)
				t_ini1 = time.time()
				
			else:
				# Second half of the cycle, t_current is calculated from time_on/2 to time_on
				
				t_current = (2*((-math.log(10))-math.log(10))/(self.time_on))*(time.time() - t_ini1) + math.log(10) # In this line we remap the time so that is goes from ln(10) to -ln(10)
					
					
			output = (25.5*math.exp(t_current))*(self.power/5.0)
			output = new_cell.clamp(output)
			
			new_cell.pi.set_PWM_dutycycle(self.vibration_pins[0], output)
			
		output=0
		new_cell.pi.set_PWM_dutycycle(self.vibration_pins[0],output)
		time.sleep(self.time_off)

	#señal click (logratimica + exponencial)
	def s_click(self):
		
		t_ini = time.time()
		
		# In this cycle the vibration signal is calculated and activated through a pwm signal
		
		while time.time() <= (t_ini + self.time_on):
			
			if time.time() < (t_ini + self.time_on/2.0):
				# First half of the cycle, t_current is calculated from 0 to time_on/2 
				
				t_current = (2*(10-1)/(self.time_on))*(time.time() - t_ini) + 1 # In this line we remap the time so that is goes from 10 to 1
				output = (255.0*math.log10(t_current))*(self.power/5.0)
				t_ini1 = time.time()
				
			else:
				# Second half of the cycle, t_current is calculated from time_on/2 to time_on
				
				t_current = (2*((-math.log(10))-math.log(10))/(self.time_on))*(time.time() - t_ini1) + math.log(10) # In this line we remap the time so that is goes from -ln(10) to ln(10)
				output = (25.5*math.exp(t_current))*(self.power/5.0)
					
			
			output = new_cell.clamp(output)
			
			new_cell.pi.set_PWM_dutycycle(self.vibration_pins[0],output)
			
		output=0
		new_cell.pi.set_PWM_dutycycle(self.vibration_pins[0],output)
		time.sleep(self.time_off)

	#señal rev-click (exponencial + logartimica)
	def s_revclick(self):
		
		t_ini = time.time()
		
		# In this cycle the vibration signal is calculated and activated through a pwm signal
		
		while time.time() <= (t_ini + self.time_on):
			
			if time.time() < (t_ini + self.time_on/2.0):
				# First half of the cycle, t_current is calculated from 0 to time_on/2
				
				t_current = (2*(math.log(10)-(-math.log(10)))/(self.time_on))*(time.time() - t_ini) + (-math.log(10)) # In this line we remap the time so that is goes from -ln(10) to ln(10)
				t_ini1 = time.time()
				output = (25.5*math.exp(t_current))*(self.power/5.0)
			else:
				# Second half of the cycle, t_current is calculated from time_on/2 to time_on

				t_current = (2*(1-10)/(self.time_on))*(time.time() - t_ini1) + 10 # In this line we remap the time so that is goes from 10 to 1
				output = (255.0*math.log10(t_current))*(self.power/5.0)
					
			
			output = new_cell.clamp(output)
			
			new_cell.pi.set_PWM_dutycycle(self.vibration_pins[0],output)
			
		output=0
		new_cell.pi.set_PWM_dutycycle(self.vibration_pins[0],output)
		time.sleep(self.time_off)


	@staticmethod
	def random_letter() -> str:
		"""Return a random letter from the alphabet including ñ

		Returns
		-------
		random_letter: str
			Random letter from the alphabet including ñ
		"""

		alfabeto_regular = "abcdefghijklmnñopqrstuvwxyz"
		return alfabeto_regular[random.randint(0,26)]
  
	@staticmethod
	def translator(letter: str) -> list:
		"""Translate a letter to a braille dot pattern, Ex. "a" -> [1, 0, 0, 0, 0, 0], " " -> [0, 0, 0, 0, 0, 0]

		Parameters
		----------
		letter : str
			Input letter to be translated.

		Returns
		-------
		braille_letter: list
			6-value boolean list representing  the input letter
		"""

		# This function translates a letter to a braille dot pattern

		letter.lower()

		regular_alphabet = " abcdefghijklmnñopqrstuvwxyz"
		braille_alphabet = [[0,0,0,0,0,0],[1,0,0,0,0,0],[1,1,0,0,0,0],[1,0,0,1,0,0],[1,0,0,1,1,0],[1,0,0,0,1,0],[1,1,0,1,0,0],[1,1,0,1,1,0],[1,1,0,0,1,0],[0,1,0,1,0,0],[0,1,0,1,1,0],[1,0,1,0,0,0],[1,1,1,0,0,0],[1,0,1,1,0,0],[1,0,1,1,1,0],[1,1,0,1,1,1],[1,0,1,0,1,0],[1,1,1,1,0,0],[1,1,1,1,1,0],[1,1,1,0,1,0],[0,1,1,1,0,0],[0,1,1,1,1,0],[1,0,1,0,0,1],[1,1,1,0,0,1],[0,1,0,1,1,1],[1,0,1,1,0,1],[1,0,1,1,1,1],[1,0,1,0,1,1]]

		braille_dictionary = dict(zip(regular_alphabet, braille_alphabet))

		return braille_dictionary[letter]

	
	def trigger(self, dot_pattern):
			
		'''This function triggers the actuator
		
			V_braille   ==> braille pattern, it's a boolean array with 6 values, ex {1,0,0,1,1,0}
			signal      ==> type of vibratino signal, it's a number between 1 and 8,    1 - Square signal
																						2 - Triangle signal
																						3 - Click signal (logarithmic + exponential)
																						4 - Ramp signal
																						5 - Exponential signal
																						6 - Sin signal
																						7 - Reverse click signal (exponential + logarithmic)
																						8 - logarithmic signal
																						
		'''
		
		for iteration_num in range(6):
			new_cell.pi.write(self.vibration_pins[iteration_num+1], dot_pattern[iteration_num])

		if self.signal_type == 1:
			self.s_square()
			
		elif self.signal_type == 2:
			
			self.s_triad()
			
		elif self.signal_type == 6:
			
			self.s_sine()
			
		elif self.signal_type == 8:
			
			self.s_log()
			
		elif self.signal_type == 5:
			
			self.s_exp()
			
		elif self.signal_type == 3:
			
			self.s_click()
			
		elif self.signal_type == 7:
			
			self.s_revclick()
			
		elif self.signal_type == 4:
			
			self.s_ramp()
			
		else:
			print("Error: wrong signal selector")

		for iteration_num in range(6):
			new_cell.pi.write(self.vibration_pins[iteration_num+1], 0)
			

	def generator(self):
		
		# This function activates all the dots in the cell going one by one
		
		for active_dot in range(0,6):
			vector_generador = [0,0,0,0,0,0]
			vector_generador[active_dot] = 1
			self.trigger(vector_generador)
		
			
	def writer(self, sentence):
		
		# This function writes the sentence in the braille cell, the sentence can be a letter, a word or a paragraph.
		
		for letter in sentence:
			caracter_braille = self.translator(letter)
			self.trigger(caracter_braille)


	def random_vibration(self):
		
		# This function actives dots randomly in the cell
		
		vector_random = [0,0,0,0,0,0]
		
		for dot in range(0,6):
			vector_random[dot] = random.randint(0,1)
		
		self.trigger(vector_random)

