def try_unlock():
	for u in Unlocks:
		cost = get_cost(u)
		if cost == {}:
			continue
		can_buy = True
		for item in cost:
			amount = cost[item]
			if num_items(item) < amount:
				can_buy = False
				break
		if can_buy:
			quick_print("Unlocking", u, "for", cost)
			unlock(u)
