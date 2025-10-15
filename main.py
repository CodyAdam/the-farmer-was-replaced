import state
import harvest_single
import harvest_multi
import move

clear()

while True:
	mode = state.get_mode()
	mode = "bone"

	if mode == "weird":
		harvest_single.do_grass_weird()
	elif mode == "hay" or mode == "wood" or mode == "carrot":
		harvest_multi.do_poly_multi()
	elif mode == "wood":
		x, y = get_pos_x(), get_pos_y()
		if (x + y) % 2 == 0:
			harvest_single.do_tree()
		else:
			harvest_single.do_grass()
	elif mode == "carrot":
		harvest_single.do_carrot()
	elif mode == "pumpkin":
		harvest_single.do_pumpkin()
	elif mode == "power":
		harvest_multi.do_power()
	elif mode == "cactus":
		harvest_single.do_cactus()
	elif mode == "bone":
		harvest_single.do_dino_alt()
	elif mode == "gold":
		harvest_multi.do_treasure()
