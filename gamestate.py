import random

# Encodes a falling block;
class BlockObj:

	# Blocks:
	#	Vertical Line
	#	Horizontal Line
	#	Diagonal Line (LR)
	#	Diagonal Line (RL)
	#	Block

	# Chance of each block appearing; Should sum to 1.0
	blockChances = [0.35, 0.35, .10, .10, .10]

	# Returns the maximum dimensions of a block
	def get_block_dims():
		return [2,2]

	# Generates a new block
	def __init__(self):
		# The generated block must have a random block type and a random position (1..7)
		r = random.randbytes(1)

		# Get the type of the block
		t = 0
		for i in range(0, len(BlockObj.blockChances)):
			chance_base256 = int(BlockObj.blockChances[i]*256).to_bytes(1, byteorder='big')
			if(r <= chance_base256):
				t = i
				break

		# Get the position of the block (use 3 LSBs)
		pos = int.from_bytes(bytes([r[0] & 0x07]), byteorder='big', signed=False)
		if pos == 7: # Avoid position 7
			pos = 0

		# Generate grid
		self.d = None
		match t:
			case 0: # V-Line
				self.d = [1,0,1,0]
			case 1: # H-Line
				self.d = [1,1,0,0]
			case 2: # Diagonal, Left-to-Right
				self.d = [1,0,0,1]
			case 3: # Diagonal, Right-to-Left
				self.d = [0,1,1,0]
			case 4: # Block
				self.d = [1,1,1,1]

		self.x = pos
		self.y = 0


	def rotate_right(self):
		temp = self.d[0]
		self.d[0] = self.d[2]
		self.d[2] = self.d[3]
		self.d[3] = self.d[1]
		self.d[1] = temp

	def rotate_left(self):
		temp = self.d[0]
		self.d[0] = self.d[1]
		self.d[1] = self.d[3]
		self.d[3] = self.d[2]
		self.d[2] = temp

	# Moves the block left (-1) or right (+1)
	def move(self, dir):
		self.x = self.x + dir
		if self.x > 7:
			self.x = 0
		elif self.x < 0:
			self.x = 7


# Encodes the state of a game; Reset after game over
class GameState():
	def __init__(self):
		# Create score
		self.score = 0
		# Game-over flag; set by `check_pile`
		self.gameOver = False

		# Initialize the block object
		self.blockObj = None

		# Initialize the pile
		self.pileObj = []
		for i in range(0, 8*8):
			self.pileObj.append(0)

	def generate_block(self):
		self.blockObj = BlockObj()

	def drop_block(self):
		# TODO
		return

	def check_pile(self):
		# TODO
		return



