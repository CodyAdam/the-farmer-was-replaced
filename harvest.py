from builtins import *
import state
import move
import utils


def water():
	if get_water() < 0.8 and num_items(Items.Water) > 100:
		use_item(Items.Water)
	

def do_carrot():
	if can_harvest():
		harvest()
	if get_ground_type() != Grounds.Soil:
		till() 
	water()
	plant(Entities.Carrot)
	move.goto(move.get_next())
	
def do_bush():
	water()
	if can_harvest():
		harvest()
	plant(Entities.Bush)
	move.goto(move.get_next())
	
def do_grass():
	if can_harvest():
		harvest()
	if get_ground_type() == Grounds.Soil:
		till() 
	move.goto(move.get_next())
	
def do_grass_weird():
	if can_harvest():
		harvest()

	x, y = get_pos_x(), get_pos_y()
	size = get_world_size()
	
	for tx in range(size):
		for ty in range(size):
			if (2 * tx + ty) % 5 == 0:
				move.goto((tx,ty))
				use_item(Items.Weird_Substance)
			
	for _ in range(size ** 2):
		if can_harvest():
			harvest()
		if get_ground_type() == Grounds.Soil:
			till() 
		move.goto(move.get_next())
	
	
def do_tree():
	water()
	if can_harvest():
		harvest()
	plant(Entities.Tree)
	move.goto(move.get_next())
	
def do_pumpkin():
	if get_entity_type() != Entities.Pumpkin and can_harvest():
		harvest()
	if get_ground_type() != Grounds.Soil:
		till() 

	iter = 0
	while not can_harvest() or iter > 50:
		iter += 1
		plant(Entities.Pumpkin)
		if num_items(Items.Fertilizer) > 1000:
			use_item(Items.Fertilizer)
		else:
			break
		
	if can_harvest():
		if len(state.data["pumpkin"]) == get_world_size() * get_world_size():
			size = get_world_size()
			
			for tx in range(size):
				for ty in range(size):
					if (2 * tx + ty) % 5 == 0:
						move.goto((tx,ty))
						use_item(Items.Weird_Substance)
			harvest()
			state.data["pumpkin"] = set()
		else:
			x, y = get_pos_x(), get_pos_y()
			if (x,y) not in state.data["pumpkin"]:
				state.data["pumpkin"].add((x,y))

	move.goto(move.get_next())
	
def do_sunflower(replant = True):
	water()
	if get_entity_type() != Entities.Sunflower and can_harvest():
		harvest()
	if get_ground_type() != Grounds.Soil:
		till() 

	if state.data["sun_planting"]:
		plant(Entities.Sunflower)
		state.data["sunflower"][(get_pos_x(), get_pos_y())] = measure()
		if len(state.data["sunflower"]) == get_world_size() * get_world_size():
			state.data["sun_planting"] = False
		move.goto(move.get_next())
	else:
		max_key, max_val = utils.max_dict(state.data["sunflower"])
		move.goto(max_key)
		x, y = get_pos_x(), get_pos_y()
		if can_harvest():
			harvest()
			if (x,y) in state.data["sunflower"]:
				state.data["sunflower"].pop((x,y))
		if len(state.data["sunflower"]) < 10:
			state.data["sun_planting"] = True

def is_sorted_col(c):
	last = -1
	for i in range(get_world_size()):
		current = state.data["cactus"][(c,i)]
		if current < last:
			return False
		last = state.data["cactus"][(c,i)]
	return True
	
def is_sorted_line(l):
	last = -1
	for i in range(get_world_size()):
		current = state.data["cactus"][(i,l)]
		if current < last:
			return False
		last = state.data["cactus"][(i,l)]
	return True
	
def do_cactus():
	if get_entity_type() != Entities.Cactus and can_harvest():
		harvest()
	if get_ground_type() != Grounds.Soil:
		till() 
	x, y = get_pos_x(), get_pos_y()

	if state.data["cactus_planting"]:
		plant(Entities.Cactus)
		state.data["cactus"][(x,y)] = measure()
		if len(state.data["cactus"]) == get_world_size() * get_world_size():
			state.data["cactus_planting"] = False
		move.goto(move.get_next())
	else:
		for col in range(get_world_size()):		
			move.goto((col,0))
			while not is_sorted_col(col):
				if get_pos_y() == get_world_size() -1:
					move.goto((col, get_pos_y() + 1))
				current = measure()
				next = measure(North)
				if current > next:
					swap(North)
					x, y = get_pos_x(), get_pos_y()
					state.data["cactus"][(x,y)] = next
					state.data["cactus"][(x,y+1)] = current
					
				move.goto((col, get_pos_y() + 1))
		for line in range(get_world_size()):		
			move.goto((0,line))
			while not is_sorted_line(line):
				if get_pos_x() == get_world_size() -1:
					move.goto((get_pos_x() + 1, line))
				current = measure()
				next = measure(East)
				if current > next:
					swap(East)
					x, y = get_pos_x(), get_pos_y()
					state.data["cactus"][(x,y)] = next
					state.data["cactus"][(x+1,y)] = current
					
				move.goto((get_pos_x() + 1, line))
		harvest()
		
		state.data["cactus"] = dict()
		state.data["cactus_planting"] = True
		state.incr_turn(get_world_size() ** 2)
		move.goto(move.get_next())


def do_dino():
	size = get_world_size()
	clear()
	move.goto((0,0))
	change_hat(Hats.Dinosaur_Hat)
	
	while move.goto(move.get_next_dino(), False):
		if get_entity_type() != Entities.Apple and can_harvest():
			harvest()
	change_hat(Hats.Dinosaur_Hat)
	state.incr_turn(size ** 2)
	
def do_treasure(data = state.data, is_clone = False):
	while get_entity_type() == Entities.Hedge:	
		if data["maze_target"] != measure():
			if is_clone:
				return
			data["maze_target"] = measure()
			data["maze_seen"] = set()
			data["maze_run"] += 1
		if num_drones() == 1 and not is_clone:
			quick_print("unstuck")
			data["maze_seen"] = set()
			
		x, y = get_pos_x(), get_pos_y()
		if data["maze_next_pos"] != None:
			move.goto(data["maze_next_pos"])
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
				continue
		for i in index_to_move:
			new_pos = dirs[i]
			if index_to_move[0] == i:
				data["maze_next_pos"] = new_pos
			elif num_drones() >= max_drones():
				break
			else:
				clone_data = dict(data)
				clone_data["maze_next_pos"] = new_pos
				state.spawn_with_data(do_treasure, clone_data)
	
	def new_maze():
		if get_entity_type() != Entities.Treasure:
			plant(Entities.Bush)
		n_substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, n_substance)
		return measure()
		
	if can_harvest() and get_entity_type() == Entities.Treasure:
		data["maze_seen"] = set()
		if data["maze_run"] == 299:
			harvest()
		data["maze_target"] = new_maze()
		data["maze_run"] += 1
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

	

		
	
def do_poly():
	comp = state.data["companion"]
	x, y = get_pos_x(), get_pos_y()
	p = None
	if (x,y) in comp:
		p = comp[(x, y)]	
		
	if p == None:
		r = random() * 3 // 1
		p = [Entities.Grass, Entities.Carrot, Entities.Tree][r]
		
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
		
	companion_plant, (cx, cy) = get_companion()
	if companion_plant:
		comp[(cx,cy)] = companion_plant
	move.goto(move.get_next())

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
				entities_list = [Entities.Bush, Entities.Grass, Entities.Carrot, Entities.Tree]
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
	
	line_data = {
		"companion": dict(state.data["companion"])
	}
	if fallback != None:
		line_data["fallback"] = fallback

	new_drone = state.spawn_with_data(
		process_line_poly,
		line_data
	)
	if new_drone != None:
		drones.append(new_drone)
		move.move_direction(North)
		state.incr_turn(size)
	state.data["poly_drones"] = drones

