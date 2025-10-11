import state
import harvest
import move

change_hat(Hats.Straw_Hat)
move.goto((0,0))

while True:
	# harvest.do_treasure()
	# continue
	mode = state.get_mode()
	mode = "cactus"
	
	if mode == "weird":
		harvest.do_grass_weird()
	elif mode == "hay" or mode == "wood" or mode == "carrot":
		harvest.do_poly_multi()
	elif mode == "wood":
		x, y = get_pos_x(), get_pos_y()
		if (x + y) % 2 == 0:
			harvest.do_tree()
		else:
			harvest.do_grass()
	elif mode == "carrot":
		harvest.do_carrot()
	elif mode == "pumpkin":
		harvest.do_pumpkin()
	elif mode == "power":
		harvest.do_sunflower()
	elif mode == "cactus":
		harvest.do_cactus()
	elif mode == "bone":
		harvest.do_dino()
	elif mode == "gold":
		harvest.do_treasure()



			