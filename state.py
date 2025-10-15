import utils
from builtins import *
import unlock

data = {
	"pumpkin": set(),
	"sunflower": dict(),
	"sun_planting": True,
	"mode": None,
	"last_mode": 999999999,
	"cactus": dict(),
	"cactus_planting": True,
	"companion": dict(),
	"maze_next_pos": None,
	"maze_seen": set(),
	"maze_target": None,
	"maze_run": 0,
	"poly_drones": [],
}


def clear_state(mode=None):
	global data
	data = {
		"pumpkin": set(),
		"sunflower": dict(),
		"sun_planting": True,
		"mode": mode,
		"last_mode": 0,
		"cactus": dict(),
		"cactus_planting": True,
		"treasure": None,
		"companion": dict(),
		"maze_next_pos": None,
		"maze_seen": set(),
		"maze_target": None,
		"maze_run": 0,
		"poly_drones": [],
	}


def incr_turn(val=1):
	global data
	data["last_mode"] += val


def set_data(new_data):
	global data
	quick_print(data)
	data = new_data
	quick_print(data)


def spawn_with_data(action, custom_data):
	def init_data_and_run():
		return action(custom_data, True)
	return spawn_drone(init_data_and_run)


def get_mode():
	global data

	min_target = 3000
	min_tick = get_world_size() ** 2
	mode = data["mode"]
	last_mode = data["last_mode"]

	data["last_mode"] += 1

	if last_mode < min_tick:
		return

	weights = {
		"hay": num_items(Items.Hay) * 1,
		"wood": num_items(Items.Wood) * 1,
		"carrot": num_items(Items.Carrot) * 1,
		"pumpkin": num_items(Items.Pumpkin) * 1,
		"power": num_items(Items.Power) * 10,
		"cactus": num_items(Items.Cactus) * 1,
		"bone": num_items(Items.Bone) * 1,
		"weird": num_items(Items.Weird_Substance) * 1,
		"gold": num_items(Items.Gold) * 1,
	}

	new_mode, _ = utils.min_dict(weights)

	if new_mode != mode:
		quick_print("Changing mode:", new_mode, "after", data["last_mode"])
		unlock.try_unlock()
		if new_mode == "bone":
			change_hat(Hats.Dinosaur_Hat)
		else:
			change_hat(Hats.Straw_Hat)

		clear_state(new_mode)
		clear()

	return new_mode
