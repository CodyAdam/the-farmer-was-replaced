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
                move.goto((tx, ty))
                use_item(Items.Weird_Substance)

    for _ in range(size**2):
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
                        move.goto((tx, ty))
                        use_item(Items.Weird_Substance)
            harvest()
            state.data["pumpkin"] = set()
        else:
            x, y = get_pos_x(), get_pos_y()
            if (x, y) not in state.data["pumpkin"]:
                state.data["pumpkin"].add((x, y))

    move.goto(move.get_next())


def do_power(replant=True):
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
            if (x, y) in state.data["sunflower"]:
                state.data["sunflower"].pop((x, y))
        if len(state.data["sunflower"]) < 10:
            state.data["sun_planting"] = True


def is_sorted_col(c):
    last = -1
    for i in range(get_world_size()):
        current = state.data["cactus"][(c, i)]
        if current < last:
            return False
        last = state.data["cactus"][(c, i)]
    return True


def is_sorted_line(l):
    last = -1
    for i in range(get_world_size()):
        current = state.data["cactus"][(i, l)]
        if current < last:
            return False
        last = state.data["cactus"][(i, l)]
    return True


def do_cactus():
    if get_entity_type() != Entities.Cactus and can_harvest():
        harvest()
    if get_ground_type() != Grounds.Soil:
        till()
    x, y = get_pos_x(), get_pos_y()

    if state.data["cactus_planting"]:
        plant(Entities.Cactus)
        state.data["cactus"][(x, y)] = measure()
        if len(state.data["cactus"]) == get_world_size() * get_world_size():
            state.data["cactus_planting"] = False
        move.goto(move.get_next())
    else:
        for col in range(get_world_size()):
            move.goto((col, 0))
            while not is_sorted_col(col):
                if get_pos_y() == get_world_size() - 1:
                    move.goto((col, get_pos_y() + 1))
                current = measure()
                next = measure(North)
                if current > next:
                    swap(North)
                    x, y = get_pos_x(), get_pos_y()
                    state.data["cactus"][(x, y)] = next
                    state.data["cactus"][(x, y + 1)] = current

                move.goto((col, get_pos_y() + 1))
        for line in range(get_world_size()):
            move.goto((0, line))
            while not is_sorted_line(line):
                if get_pos_x() == get_world_size() - 1:
                    move.goto((get_pos_x() + 1, line))
                current = measure()
                next = measure(East)
                if current > next:
                    swap(East)
                    x, y = get_pos_x(), get_pos_y()
                    state.data["cactus"][(x, y)] = next
                    state.data["cactus"][(x + 1, y)] = current

                move.goto((get_pos_x() + 1, line))
        harvest()

        state.data["cactus"] = dict()
        state.data["cactus_planting"] = True
        state.incr_turn(get_world_size() ** 2)
        move.goto(move.get_next())


def create_body(pos=None, prev=None, next=None, skipped=[]):
    if pos == None:
        pos = (get_pos_x(), get_pos_y())
    return {"prev": prev, "next": next, "pos": pos, "skipped": skipped}


def generatePath(iterations):
    # Generate Moore curve using L-system
    # L-system for Moore curve
    # Axiom: LFL+F+LFL
    # Rules: L → -RF+LFL+FR-, R → +LF-RFR-FL+

    axiom = "LFL+F+LFL"
    current = axiom

    for _ in range(iterations):
        next_string = ""
        for char in current:
            if char == "L":
                next_string += "-RF+LFL+FR-"
            elif char == "R":
                next_string += "+LF-RFR-FL+"
            else:
                next_string += char
        current = next_string

    return list(current)


def generate_dino_path_mapping(size):
    start = (0, size // 2)
    current = start
    index = 0
    iterations = int(math.log2(size)) - 1
    path = generatePath(iterations)
    direction = (1, 0)
    mapping = {}

    while len(path) > 0:
        op = path.pop(0)
        if op == "L" or op == "R":  # skip
            continue
        if op == "F":
            mapping[current] = (move.get_direction_from_vec(direction), index)
            current = utils.add(current, direction)
            index += 1
        if op == "+":
            # rotate right
            direction = (direction[1], -direction[0])
        if op == "-":
            # rotate left
            direction = (-direction[1], direction[0])

    mapping[current] = (move.get_direction_from_vec(utils.sub(start, current)), index)

    return mapping


path_map, path_array = generate_dino_path_mapping(get_world_size())
max_value = get_world_size() ** 2


def do_dino_alt():
    global path_map
    clear()
    change_hat(Hats.Dinosaur_Hat)

    size = get_world_size()
    head = create_body()
    tail = head
    length = 1
    body_parts = set([head["pos"]])
    apple = measure()
    _, apple_value = path_map[apple]

    while True:
        x, y = get_pos_x(), get_pos_y()
        direction, index = path_map[(x, y)]
        if apple_value < index:
            dist = apple_value - index + max_value
        else:
            dist = apple_value - index
        skip = None
        if length < (size**2) // 2:
            for neighbor in move.get_neighbors((x, y)):
                if neighbor in path_map and neighbor not in body_parts:
                    _, ni = path_map[neighbor]
                    if apple_value < ni:
                        ndist = apple_value - ni + max_value
                    else:
                        ndist = apple_value - ni

                    if ndist < dist:
                        dist = ndist
                        skip = (neighbor, ni)
        skipped_pos = []
        if skip:
            pos, ni = skip
            if ni > index:
                # Skip forward: get positions between current+1 and skip
                skipped_pos = path_array[index + 1 : ni]
            else:
                skipped_pos = path_array[index:] + path_array[:ni]
            move.goto(pos)
        else:
            if not move.move_direction(direction):
                break
        x, y = get_pos_x(), get_pos_y()
        # Add new head
        new_head = create_body((x, y), head, None, skipped_pos)
        head["next"] = new_head
        head = new_head
        body_parts.add((x, y))
        for pos in skipped_pos:
            body_parts.add(pos)

        if get_entity_type() == Entities.Apple:
            length += 1
            apple = measure()
            _, apple_value = path_map[apple]
        else:
            # Remove tail
            if tail["pos"] in body_parts:
                body_parts.remove(tail["pos"])
            for pos in tail["skipped"]:
                if pos in body_parts:
                    body_parts.remove(pos)
            tail = tail["next"]
            tail["prev"] = None

    change_hat(Hats.Dinosaur_Hat)
    state.incr_turn(size**2)


def do_poly():
    comp = state.data["companion"]
    x, y = get_pos_x(), get_pos_y()
    p = None
    if (x, y) in comp:
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
        comp[(cx, cy)] = companion_plant
    move.goto(move.get_next())
