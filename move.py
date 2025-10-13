from builtins import *
import utils


def goto(pos, wrapping = True):
	#quick_print(pos)
	x, y = pos
	dx, dy = x - get_pos_x(), y - get_pos_y()
	size = get_world_size()
	
	# wrapping
	if wrapping:
		if abs(dx) > size // 2:
			dx = dx - size * (dx > 0) + size * (dx < 0)
		if abs(dy) > size // 2:
			dy = dy - size * (dy > 0) + size * (dy < 0)
			
	for _ in range(0, abs(dx)):
		if dx > 0:
			if not move(East):
				return False
		else:
			if not move(West):
				return False
	for _ in range(0, abs(dy)):
		if dy > 0:
			if not move(North):
				return False
		else:
			if not move(South):
				return False
	return True
	

def get_next():
	x, y = get_pos_x(), get_pos_y()
	if y == get_world_size() - 1:
		x += 1
	y += 1
	return (x,y)

def get_next_line():
	x, y = get_pos_x(), get_pos_y()
	size = get_world_size()
	return ((x + 1) % size, y)

def get_ordered_direction_to(pos):
	# get the direction array like [North, East, South, West], but sorted so that the first direction is the one that is closest to the target
	target_x, target_y = pos
	x, y = get_pos_x(), get_pos_y()
	dx = target_x - x
	dy = target_y - y

	directions = [North, East, South, West]

	def score_direction(direction):
		# returns a value (lower is closer to target)
		if direction == North:
			return abs(dx) + abs(dy-1)
		elif direction == South:
			return abs(dx) + abs(dy+1)
		elif direction == East:
			return abs(dx-1) + abs(dy)
		elif direction == West:
			return abs(dx+1) + abs(dy)
		return abs(dx) + abs(dy)

	scored_dirs = []
	for direction in directions:
		scored_dirs.append((score_direction(direction), direction))

	# manual selection sort (since sort is not allowed)
	n = len(scored_dirs)
	for i in range(n):
		min_idx = i
		for j in range(i + 1, n):
			if scored_dirs[j][0] < scored_dirs[min_idx][0]:
				min_idx = j
		# Swap the found minimum element with the first element
		scored_dirs[i], scored_dirs[min_idx] = scored_dirs[min_idx], scored_dirs[i]

	ordered = []
	for pair in scored_dirs:
		ordered.append(pair[1])
	return ordered

def get_pos_from_direction(direction):
	x, y = get_pos_x(), get_pos_y()
	offsets = {
		North: (0, 1),
		South: (0, -1),
		East: (1, 0),
		West: (-1, 0)
	}
	dx, dy = offsets[direction]
	return (x + dx, y + dy)
	
dino_cycle_alt = False
def get_next_dino():
	global dino_cycle_alt
	x, y = get_pos_x(), get_pos_y()
	size = get_world_size()
	odd = size % 2 == 1
	is_top = y == size - 1
	is_pre_bot = y == 1
	is_bot = y == 0
	is_bot_left = (x,y) == (0, 0)
	is_even_col = x % 2 == 0
	
	
	if is_bot_left:
		return (0, 1)
	if is_bot:
		dino_cycle_alt = not dino_cycle_alt
		return (0, 0)
	if odd:
		if dino_cycle_alt: 
			if (x,y) == (size-2, size-1):
				return (x+1, y)
			if (x,y) == (size-1, size-1): 
				return (x, y-1)
		if x == size - 2:
			if (x+y) % 2 == 0:
				return (x+1, y)
			else:
				return (x, y-1)
		elif x == size -1:
			if (x+y) % 2 == 1:
				return (x, y-1)
			else:
				return (x-1, y)
	if (x,y) == (size - 1 - size % 2, 1):
		return (x, 0)

	if(is_top and is_even_col) or (is_pre_bot and not is_even_col):
		return (x+1, y)
		
	if x % 2 == 0:
		y += 1
	else:
		y -= 1
	return utils.clamp_pos((x,y))
	
def move_direction(direction):
	return move(direction)