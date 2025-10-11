import state

def test(data = state.data):
	print(data["maze_dir_index"])
	while data["maze_dir_index"] > 0:
		data["maze_dir_index"] -= 1
		move(North)
	do_a_flip()

for i in range(16):
	data_clone = dict(state.data)
	data_clone["maze_dir_index"] = i+1
	state.spawn_with_data(test, data_clone)
	move(East)