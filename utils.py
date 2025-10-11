def max_dict(d):
	max_val = None
	max_key = None
	for key in d:
		val = d[key]
		if max_val == None or max_val < val:
			max_val = val
			max_key = key
	return max_key, max_val

def min_dict(d):
	min_val = None
	min_key = None
	for key in d:
		val = d[key]
		if min_val == None or min_val > val:
			min_val = val
			min_key = key
	return min_key, min_val

def clamp_pos(pos):
	x, y = pos
	size = get_world_size()
	clamp_x = max(min(size-1, x), 0)
	clamp_y = max(min(size-1, y), 0)
	return (clamp_x, clamp_y)
	