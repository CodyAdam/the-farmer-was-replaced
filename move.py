from builtins import *
import utils


def goto(pos, wrapping=True):
	# quick_print(pos)
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
	return (x, y)


def get_next_line():
	x, y = get_pos_x(), get_pos_y()
	size = get_world_size()
	return ((x + 1) % size, y)


def get_ordered_direction_to(pos):
	# Returns [North, East, South, West] prioritized according to dx/dy sign using a dict
	target_x, target_y = pos
	x, y = get_pos_x(), get_pos_y()
	dx = target_x - x
	dy = target_y - y

	sdx = utils.sign(dx)
	sdy = utils.sign(dy)

	dir_map = {
		(0, 0): [North, East, South, West],  # Already there, arbitrary
		(1, 0): [East, North, South, West],  # Go East first
		(-1, 0): [West, North, South, East],  # Go West first
		(0, 1): [North, East, West, South],  # Go North first
		(0, -1): [South, East, West, North],  # Go South first
		(1, 1): [North, East, West, South],  # Prefer North then East
		(1, -1): [South, East, North, West],  # Prefer South then East
		(-1, 1): [North, West, East, South],  # Prefer North then West
		(-1, -1): [South, West, North, East],  # Prefer South then West
	}

	# Fallback if not found (should not hit)
	return dir_map[(sdx, sdy)]


def get_pos_from_direction(direction, pos=None):
	if pos == None:
		pos = (get_pos_x(), get_pos_y())
	x, y = pos
	offsets = {North: (0, 1), South: (0, -1), East: (1, 0), West: (-1, 0)}
	dx, dy = offsets[direction]
	return (x + dx, y + dy)


def get_neighbors(pos):
	x, y = pos
	return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def get_direction_from_vec(vector):
	return {
		(0, 1): North,
		(0, -1): South,
		(1, 0): East,
		(-1, 0): West,
	}[vector]


def move_direction(direction):
	return move(direction)
