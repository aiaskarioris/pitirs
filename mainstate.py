import os
import time
from enum import Enum

class MainStateEnum(Enum):
	wait_to_start = 0
	playing = 1
	game_over = 2
	exception = 3

# Renderer for debugging purposes
class CLIRenderer:
	def __init__(self):
		return

	def set_pixels(self, p):
		# Clear screen
		os.system("clear")
		# print("")
		for l in range(0, 8):
			for c in range(0, 8):
				if p[l*8 + c] == 1:
					print('█', end='')
				else:
					print(' ', end='')
				print("")

class MainState():
	def __init__(self):
		self.renderer = CLIRenderer() # or SenseHat()
		self.state = MainStateEnum.wait_to_start
		self.frame = 0
		self.refresh_time_ms = 50
		self.game = None

	# Main loop
	def run(self):
		while(True):
			if self.state == MainStateEnum.wait_to_start:
				self.wait_to_start_loop()

			elif self.state == MainStateEnum.playing:
				self.playing_loop()

			elif self.state == MainStateEnum.game_over:
				self.game_over_loop()

			elif self.state == MainStateEnum.exception:
				self.exception_loop()

		self.frame += 1
		time.sleep(self.refresh_time_ms / 1000)

	# Sub-Loops; Each loop can freely display things on screen and change the program's states
	def wait_to_start_loop(self):
		# Wait for input
		if ... :
			# Still waiting...
			# Do an animation based on `self.frame` value
		else:
			# A new game is starting
			self.game = GameState()
			self.state = MainState.playing
		return

	def playing_loop(self):
		# Generate a random block if we don't have one (just started playing or prev. one was piled)
		if self.game.block_obj == None:
			self.game.generate_block()
		# Check input and apply effect to block

		# Allow block to drop by 1 pixel; The block may enter the pile in this function (this clearing it)
		self.game.drop_block()

		# Check if the pile has any full lines and drop remaining lines; score may be updated
		self.game.check_pile()

		# Render current state
			# Draw block
			# Draw the pile

		# `check_pile` may generate a game-over; Check if this is the case
		if self.game_over == True:
			self.state = MainState.game_over

		return

	def game_over_loop(self):
		# Create a buffer and store the score as text into it ((8xlen_of_score) x 8)

		# In a 8x8 array, copy a part of the buffer above depending on `self.frame` (= offset)
		d = []
		for i in range(0, 64):
			d.append(0)

		# Display the 8x8 array
		self.renderer.set_pixels(d)
		return

	def exception_loop(self):

		return
