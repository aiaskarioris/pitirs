import random

# Encodes a falling block;
class BlockObj:

	# Blocks:
	#	Vertical Line
	#	Horizontal Line
	#	Diagonal Line (LR)
	#	Diagonal Line (RL)
	#	Block

	blockChances = [77,		154,	192,	217,	243]
	blockPalette = [[255,64,0],	[127,127,0],	[64,255,0],	[0,127,127],	[127, 20, 127]]

	# Returns the maximum dimensions of a block
	def get_block_dims():
		return [2,2]

	# Generates a new block
	def __init__(self):
		# The generated block must have a random block type and a random position (1..7)
		r = random.randbytes(1)

		# Get the type of the block
		t = 0

		if r[0] <= BlockObj.blockChances[0]:
			t = 0
		elif r[0] >= BlockObj.blockChances[len(BlockObj.blockChances)-1]:
			t = len(BlockObj.blockChances)-1
		else:
			for i in range(1, len(BlockObj.blockChances)-1):
				# The generated number falls between two random chances
				if r[0] >= (BlockObj.blockChances[i]) and (r[0] <= BlockObj.blockChances[i+1]):
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

		# Set position
		self.x = pos
		self.y = 0

		# Set color
		self.palette = BlockObj.blockPalette[t]

		print("New block: Type " + str(t) + " , at " + str(pos))


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
		# Game-over flag; set by `check_overflow`
		self.gameOver = False

		# Initialize the block object
		self.blockObj = None

		# Initialize the pile
		self.pileObj = []
		for i in range(0, 8*8):
			self.pileObj.append(0)

	def generate_block(self):
		print("Generating block")
		self.blockObj = BlockObj()

	def drop_block(self):
		block = self.blockObj

		# Check what's underneath the block; we'll check each pixel independantly
		base_pos = block.y * 8 + block.x
		should_goto_pile = False
		for i in range(0, 4):
			# Skip empty pixels
			if block.d[i] == 0:
				continue

			pixel_pos = base_pos + (i%2)
			if i >= 2:
				pixel_pos = pixel_pos + 8
			print("testing pp " +str(pixel_pos))

			new_pixel_pos = pixel_pos + 8
			# Check if the new position of the pixel reaches the ground
			if new_pixel_pos >= 64:
				should_goto_pile = True
				break;
			# Check if the new position of the pixel overlaps with the pile
			if self.pileObj[new_pixel_pos] == 1:
				should_goto_pile = True
				break;

		# If at least one pixel raised `should_goto_pile` then move the block to the pile (duh)
		if should_goto_pile:
			print("Block entered the pile.")
			for i in range(0,4):
				if block.d[i] == 0:
					continue

				pixel_pos = base_pos + (i%2)
				if i >= 2:
					pixel_pos = pixel_pos + 8
				self.pileObj[pixel_pos] = 1

			# Clear the block
			self.blockObj = None

		# Otherwise the block is free to fall by one step
		else:
			print("Block fell. " + str(block.y))
			block.y = block.y + 1

		return

	def check_overflow(self):
		pile = self.pileObj
		overflow = False
		for i in range(0, 8):
			overflow = overflow or pile[i]

		self.gameOver = overflow

	def check_pile(self):
		pile = self.pileObj

		# If a line is cleared the score will go up
		# A higher score increase is awarded if more than one line is cleared
		# with one move
		score = 0

		# From bottom to top, check which lines are completed
		for line in range(7, -1, -1):
			print("check_pile: Checking line " + str(line))
			# Check this if line is full
			is_full = True
			for i in range(0,8):
				is_full = is_full and pile[line*8 + i]

			# If the line is full, clear it and shift all other lines down
			if is_full:
				print("\tLine" + str(line) + " is full!")
				score = (score*2) + 10
				# Move all lines above the full one down once
				for mv_line in range(line-1, -1, -1):
					print("\tmoving line " + str(mv_line))
					self.move_line_down(mv_line)
				# Clear the top line (line 0)
				for i in range(0, 8):
					pile[i] = 0

		# Update score
		print("Score went up by " + str(score))
		self.score = self.score + score

		return

	def move_line_down(self, line_no):
		for i in range(0, 8):
			src_idx = line_no * 8 + i
			dst_idx = (line_no+1) * 8 + i
			self.pileObj[dst_idx] = self.pileObj[src_idx]



