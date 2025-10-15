from builtins import *
import state
import move
import utils


MAZE_MAX_DRONES = 10


def water():
	if get_water() < 0.8 and num_items(Items.Water) > 100:
		use_item(Items.Water)


def do_treasure(data=state.data, is_clone=False):
	while get_entity_type() == Entities.Hedge:
		x, y = get_pos_x(), get_pos_y()
		if data["maze_target"] != measure():
			data["maze_target"] = measure()
			data["maze_seen"] = set()
			data["maze_run"] += 1
		if num_drones() == 1 and not is_clone:
			quick_print("unstuck")
			data["maze_seen"] = set()

		if data["maze_next_pos"] != None:
			move.goto(data["maze_next_pos"], False)
		if not get_entity_type() == Entities.Hedge:
			break
		dirs_face = move.get_ordered_direction_to(data["maze_target"])
		dirs = []
		for direction in dirs_face:
			dirs.append(move.get_pos_from_direction(direction))
		x, y = get_pos_x(), get_pos_y()
		data["maze_seen"].add((x, y))
		index_to_move = []
		for i in range(4):
			if dirs[i] in data["maze_seen"]:
				continue
			if can_move(dirs_face[i]):
				index_to_move.append(i)
		if len(index_to_move) == 0:
			if is_clone:
				return
			else:
				move.move_direction(utils.random_direction())
				continue
		for i in index_to_move:
			new_pos = dirs[i]
			if index_to_move[0] == i:
				data["maze_next_pos"] = new_pos
			elif num_drones() >= MAZE_MAX_DRONES:
				break
			else:
				clone_data = dict(data)
				clone_data["maze_next_pos"] = new_pos
				state.spawn_with_data(do_treasure, clone_data)

	def new_maze():
		if get_entity_type() != Entities.Treasure:
			plant(Entities.Bush)
		n_substance = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, n_substance)
		return measure()

	if can_harvest() and get_entity_type() == Entities.Treasure:
		data["maze_seen"] = set()
		data["maze_target"] = new_maze()
		data["maze_run"] += 1
		if data["maze_run"] == 300:
			harvest()
		quick_print("maze_run", data["maze_run"])
		state.incr_turn(get_world_size() ** 2)
		if is_clone:
			state.spawn_with_data(do_treasure, dict(data))
	else:
		# init
		if not is_clone:
			data["maze_run"] = 0
			data["maze_seen"] = set()
			data["maze_target"] = new_maze()

	state.data = data


def process_line_poly(data, is_clone=False):
	comp = data["companion"]
	size = get_world_size()
	line_y = get_pos_y()

	# Get fallback from data dictionary directly, default to None if key missing
	if "fallback" in data:
		fallback = data["fallback"]
	else:
		fallback = None

	for x in range(size):
		move.goto((x, line_y))
		pos = (x, line_y)

		p = None
		if pos in comp:
			p = comp[pos]

		if p == None:
			if fallback != None:
				p = fallback
			else:
				# Default fallback random:
				entities_list = [
					Entities.Bush,
					Entities.Grass,
					Entities.Carrot,
					Entities.Tree,
				]
				r = int(random() * len(entities_list))
				p = entities_list[r]

		if can_harvest():
			harvest()

		if p == Entities.Bush:
			water()
			plant(Entities.Bush)
		elif p == Entities.Grass:
			if get_ground_type() == Grounds.Soil:
				till()
		elif p == Entities.Carrot:
			water()
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Carrot)
		elif p == Entities.Tree:
			water()
			plant(Entities.Tree)

		companion_result = get_companion()
		if companion_result != None:
			companion_plant, (cx, cy) = companion_result
			if companion_plant:
				comp[(cx, cy)] = companion_plant

	return comp


def do_poly_multi(fallback=None):
	size = get_world_size()
	drones = state.data["poly_drones"]

	x = get_pos_x()
	y = get_pos_y()

	if x != 0:
		move.goto((0, y))

	i = 0
	while i < len(drones):
		drone_handle = drones[i]
		if has_finished(drone_handle):
			line_comp = wait_for(drone_handle)
			if line_comp:
				for pos in line_comp:
					state.data["companion"][pos] = line_comp[pos]
			drones.pop(i)
		else:
			i += 1

	line_data = {"companion": dict(state.data["companion"])}
	if fallback != None:
		line_data["fallback"] = fallback

	new_drone = state.spawn_with_data(process_line_poly, line_data)
	if new_drone != None:
		drones.append(new_drone)
		move.move_direction(North)
		state.incr_turn(size)
	state.data["poly_drones"] = drones


def plant_line(data, is_clone=False):
	entity = data["entity"]
	tilt = data["tilt"]
	measures = dict()
	size = get_world_size()
	for i in range(size):
		if can_harvest():
			harvest()
		if tilt and get_ground_type() != Grounds.Soil:
			till()
		water()
		plant(entity)
		measures[(get_pos_x(), get_pos_y())] = measure()
		state.incr_turn(1)
		if i != size - 1:
			move.move_direction(East)
	return measures


def plant_all(entity, till=False):
	move.goto((0, 0))
	size = get_world_size()
	measures = dict()
	drones = []
	for _ in range(size):
		drone = None
		while drone == None:
			drone = state.spawn_with_data(plant_line, {"entity": entity, "tilt": till})
		drones.append(drone)
		move.move_direction(North)
		state.incr_turn(1)
	for drone in drones:
		data = wait_for(drone)
		for key in data:
			measures[key] = data[key]
	return measures


def collect_at(data, is_clone=False):
	pos = data["pos"]
	move.goto(pos)
	while not can_harvest():
		pass
	harvest()

def do_power():
	values = plant_all(Entities.Sunflower, True)
	size = get_world_size()
	move.goto((size//2, size//2))
	ranks = dict()
	for pos in values:
		value = values[pos]
		if value not in ranks:
			ranks[value] = []
		ranks[value].append(pos)
	
	for rank in range(15, 6, -1):
		rank_positions = ranks[rank]
		if not rank_positions:
			continue
		for pos in ranks[rank]:
			while not state.spawn_with_data(collect_at, {"pos": pos}):
				pass
		while num_drones() > 1:
			pass
			

