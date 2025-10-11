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