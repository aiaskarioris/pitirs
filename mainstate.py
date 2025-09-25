import os
import time
from enum import Enum

from gamestate import GameState

class MainStateEnum(Enum):
	wait_to_start = 0
	playing = 1
	game_over = 2
	exception = 3

# Renderer for debugging purposes
class CLIRenderer:
	def __init__(self):

		# Create the LED gird represantation
		self.p = []
		for i in range(0, 64):
			p.append([0, 0, 0])
		return

    # for game_over_loop
	def show_message(self, text):
		print("[CLI]", text)

    # for game_over_loop
	def clear(self):
		print("[CLI] clear")

	def set_pixels(self, p):
		# Store new pixels
		self.p = p

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

	def get_pixels(self):
		return self.p


class MainState():
	def __init__(self):
		self.renderer = CLIRenderer() # or SenseHat()
		self.state = MainStateEnum.wait_to_start
		self.frame = 0
		self.refresh_time_ms = 50
		self.game = None
		self.pixels = []

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

	### State Functions ###########################################################################

	# Sub-Loops; Each loop can freely display things on screen and change the program's states
	def wait_to_start_loop(self):
		# Wait for input
		if False:
			# Still waiting...
			# Do an animation based on `self.frame` value
			0
		else:
			# A new game is starting
			self.game = GameState()
			self.state = MainStateEnum.playing
		return

	def playing_loop(self):
		# Generate a random block if we don't have one (just started playing or prev. one was piled)
		if self.game.blockObj == None:
			self.game.generate_block()
		# Check input and apply effect to block

		# Allow block to drop by 1 pixel; The block may enter the pile in this function (thus clearing it)
		self.game.drop_block()

		# Check if the pile has any full lines and drop remaining lines; score may be updated
		self.game.check_pile()

		# Render current state; Create the 8x8 grid first and pass it to `.set_pixels` once
		self.clear_screen()
		self.draw_block()
		self.draw_pile()
		self.renderer.set_pixels(self.pixels)

		# `check_pile` may generate a game-over; Check if this is the case
		if self.game.gameOver == True:
			self.state = MainStateEnum.game_over

		return

	def game_over_loop(self):
	    try:
	        while self.state == MainStateEnum.game_over:
			    self.renderer.show_message("GAME OVER")
	    except KeyboardInterrupt:
	        self.renderer.clear()

	def exception_loop(self):
		# TODO
		return

	### Drawing Functions #########################################################################
	def clear_screen(self):
		self.pixels = []
		for i in range(0, 64):
			self.pixels.append([0, 0, 0])
		return

	def draw_block(self):
		# Get a reference
		p = self.pixels
		block = self.gamestate.blockObj

		# Draw the block in columns
		idx = block.x + block.y * 8

		# Draw first column
		if block.d[0] == 1:
			p[idx] = block.color
		if block.d[2] == 1:
			p[idx+8] = block.color

		# Draw second column; If the block is on the right-most column, wrap
		if block.x < 7:
			idx = block.x + 1 + block.y * 8
		else:
			idx = block.y * 8

		if block.d[1] == 1:
			p[idx] = block.color
		if block.d[3] == 1:
			p[idx+8] = block.color

		return

	def draw_pile(self):
		pileCol = [80, 80, 80]
		pileObj = self.gamestate.pileObj

		p = self.pixels

		for i in range(0, 64):
			if pileObj.d[i] == 1:
				p[i] = pileCol

		return
