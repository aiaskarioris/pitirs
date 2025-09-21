'''
	XO	XX	XO	XX
	XO	OO	OX	XX
'''


# Encodes a falling block;
class ClassObj:
	# Returns the maximum dimensions of a block
	def get_block_dims():
		return [2,2]

	def generate_block():



# Encodes the state of a game; Reset after game over
class GameState():
	def __init__():
		# Create score
		self.score = 0
		# Game-over flag; set by `check_pile`
		self.game_over = False

		# Initialize the pile
		self.pileObj = []
		for i in range(0, 8*8):
			self.pileObj.append(0)

