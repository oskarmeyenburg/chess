import numpy

import engine


def valid_position(position):
    return 0 <= position[0] <= 7 and 0 <= position[1] <= 7


def get_fields_threatened(id, grid_edited, king_pos, simulate_threat=1):
    fields_threatened = []
    attackers = []
    for x, y in numpy.ndindex(grid.shape):
        if grid_edited[x, y] != 0 and grid_edited[x, y] % 2 != id % 2:
            moves = get_possible_moves(
                grid_edited,
                grid_edited[x, y],
                [x, y],
                fields_threatened,
                [],
                simulate_threat,
            )
            for move in moves:
                if move == king_pos and [x, y] not in attackers:
                    attackers.append([x, y])
                fields_threatened.append(move)
    return fields_threatened, attackers


def iterate_moves(
    j_possible,
    i_max,
    coords_position,
    id,
    fields_threatened,
    grid,
    get_way,
    coords_goal,
):
    possible_moves = []
    for j in j_possible:
        way = []
        for i in range(1, i_max):
            position = [
                coords_position[0] + i * j[0],
                coords_position[1] + int(i * j[1]),
            ]
            if not valid_position(position):
                continue
            if (
                grid[position[0], position[1]] % 2 == id % 2
                and grid[position[0], position[1]] != 0
            ):
                break
            if position not in possible_moves and position not in way:
                way.append(position)
            if get_way:
                if grid[position[0], position[1]] == int(not id % 2) + 10:
                    while position in way:
                        way.remove(position)
                    return way
            if id not in (5, 6):
                if grid[position[0], position[1]] != 0:
                    break
        for i in way:
            possible_moves.append(i)
    return possible_moves


def get_possible_moves(
    grid, id, coords_position, fields_threatened, coords_goal, simulate_threat
):
    global castle_moves

    possible_moves = []
    get_way = False
    if simulate_threat == 2:
        get_way = True
    j_possible = ()
    i_max = 0
    if id == 1 or id == 2:  # bauer
        i_max = 2
        j_possible = [[0, -1], [-1, -1], [1, -1]]
        if id % 2 != 1:
            for j in enumerate(j_possible):
                j_possible[j[0]] = (j[1][0] * -1, j[1][1] * -1)
        if simulate_threat != 1:
            for i in j_possible[1:]:
                if valid_position(
                    (
                        coords_position[0] + i[0],
                        coords_position[1] + int((id - 1.5) * 2),
                    )
                ):
                    if (
                        grid[
                            coords_position[0] + i[0],
                            coords_position[1] + int((id - 1.5) * 2),
                        ]
                        == 0
                    ):
                        j_possible.remove(i)
            if coords_position[1] == (id - 2) * -5 + 1:
                i_max += 1
            if (
                valid_position(
                    (coords_position[0], coords_position[1] + int((id - 1.5) * 4))
                )
                and grid[coords_position[0], coords_position[1] + int((id - 1.5) * 4)]
                != 0
            ):
                i_max = 2
        if (
            valid_position(
                (coords_position[0], coords_position[1] + int((id - 1.5) * 2))
            )
            and grid[coords_position[0], coords_position[1] + int((id - 1.5) * 2)] != 0
            or simulate_threat == 1
        ):
            j_possible.pop(0)

    elif id == 3 or id == 4:  # turm
        i_max = 8
        j_possible = ((1, 0), (-1, 0), (0, 1), (0, -1))
    elif id == 7 or id == 8:  # läufer
        i_max = 8
        j_possible = ((1, 1), (-1, -1), (1, -1), (-1, 1))
    elif id == 5 or id == 6:  # pferd
        i_max = 2
        j_possible = (
            (1, 2),
            (2, 1),
            (-1, 2),
            (-2, 1),
            (-1, -2),
            (-2, -1),
            (1, -2),
            (2, -1),
        )
    elif id == 9 or id == 10:  # dame
        i_max = 8
        j_possible = (
            (1, 1),
            (-1, -1),
            (1, -1),
            (-1, 1),
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        )
    elif id == 11 or id == 12:  # könig
        i_max = 2
        j_possible = (
            (1, 1),
            (-1, -1),
            (1, -1),
            (-1, 1),
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        )
    possible_moves = iterate_moves(
        j_possible,
        i_max,
        coords_position,
        id,
        fields_threatened,
        grid,
        get_way,
        coords_goal,
    )
    if (id == 11 or id == 12) and simulate_threat == 0:  # könig
        castle_moves = [
            [[None, None], [None, None], [None, None], [None, None]],
            [[None, None], [None, None], [None, None], [None, None]],
        ]
        for tower in range(2):
            if castling[int(tower + (id % 2) * 2)] and not is_threatened[int(id % 2)]:
                can_castle = True
                y = turn * 7
                for x in range(max(2, min(tower * 7, 4) + 1), max(tower * 7, 4)):
                    fields_threatened, attacker = get_fields_threatened(
                        id, grid, coords_position, 1
                    )
                    if grid[x, y] != 0 or [x, y] in fields_threatened:
                        can_castle = False
                        break
                if can_castle:
                    castle_moves[tower] = [
                        [4, coords_position[1]],
                        [tower * 7, coords_position[1]],
                        [tower * 6 + int(not tower) * 2, coords_position[1]],
                        [tower * 5 + int(not tower) * 3, coords_position[1]],
                    ]
                    possible_moves.append(castle_moves[tower][2])

    if simulate_threat == 0 and id == 11 or id == 12:
        moves = possible_moves.copy()
        grid_edited = grid.copy()
        grid_edited[coords_position[0], coords_position[1]] = 0
        for move in moves:
            grid_edited = grid.copy()
            grid_edited[coords_position[0], coords_position[1]] = 0
            # if grid_edited[move[0], move[1]] % 2 != id % 2:
            grid_edited[move[0], move[1]] = id
            fields_threatened, attackers = get_fields_threatened(
                id, grid_edited, coords_position, 1
            )
            # for move in moves:
            if move in fields_threatened:
                possible_moves.remove(move)
    return possible_moves


def can_interfere(attackers, king_position):
    can_stop = []
    for attacker in attackers:
        for i in get_possible_moves(
            grid, grid[attacker[0], attacker[1]], attacker, [], king_position, 2
        ):
            can_stop.append(i)
    for attacker in attackers:
        can_stop.append(attacker)
    return can_stop


def move(id, coords_position, coords_goal, grid_in, simulate=False):
    global castling, turn, graveyard

    grid = grid_in.copy()
    for tower in range(2):
        if not castle_moves[tower][1][1] is None:
            if (
                not simulate
                and (id == 11 or id == 12)
                and list(coords_goal) == castle_moves[tower][2]
            ):
                grid[castle_moves[tower][2][0], castle_moves[tower][2][1]] = id
                grid[castle_moves[tower][3][0], castle_moves[tower][3][1]] = int(
                    (4 - (id % 2))
                )
                grid[castle_moves[tower][0][0], castle_moves[tower][0][1]] = 0
                grid[castle_moves[tower][1][0], castle_moves[tower][1][1]] = 0
                return grid

    if not simulate:
        if grid[coords_goal[0], coords_goal[1]] != 0:
            graveyard.append(grid[coords_goal[0], coords_goal[1]])
        if id in (3, 4) and coords_position in ((0, 7), (7, 7), (0, 0), (7, 0)):
            index = ((0, 7), (7, 7), (0, 0), (7, 0)).index(coords_position)
            castling[index] = False
        if id >= 11:
            castling[int(int(id % 2) * 2) : int(int(id % 2) * 2 + 2)] = (False, False)
    grid[coords_position[0], coords_position[1]] = 0
    grid[coords_goal[0], coords_goal[1]] = id
    if not simulate and (
        id == 1 and coords_goal[1] == 0 or id == 2 and coords_goal[1] == 7
    ):
        engine.update(grid, [], turn, graveyard, [], [False, False])
        grid[coords_goal[0], coords_goal[1]] = engine.get_pawn_promotion(turn)
    return grid


def check_move(coords_position, coords_goal):
    global grid, last_position, possible_moves, is_threatened, interfere, turn, result

    id = grid[coords_position[0], coords_position[1]]
    if coords_position != last_position:
        possible_moves = get_possible_moves(
            grid, id, coords_position, [], coords_goal, 0
        )
        if id < 11 and not interfere is None:
            for mov in possible_moves.copy():
                if not mov in interfere:
                    possible_moves.remove(mov)
        grid_edited = grid.copy()
        if grid[coords_position[0], coords_position[1]] != 11 + int(not turn):
            for goal in possible_moves.copy():
                grid_edited_2 = move(id, coords_position, goal, grid_edited, True)
                for x, y in numpy.ndindex(grid.shape):
                    if grid[x, y] == 11 + int(not turn):
                        fields_threatened, attackers = get_fields_threatened(
                            id, grid_edited_2, [x, y], 0
                        )
                        if [x, y] in fields_threatened:
                            while goal in possible_moves:
                                possible_moves.remove(goal)
                        break
        last_position = coords_position
    if (
        (coords_goal is not None)
        and list(coords_goal) in possible_moves
        and coords_position != coords_goal
    ):
        grid = move(id, coords_position, coords_goal, grid)
        turn = int(not id % 2)
        for x, y in numpy.ndindex(grid.shape):
            if grid[x, y] == 11 + int(not turn):
                fields_threatened, attackers = get_fields_threatened(
                    turn, grid, [x, y], 0
                )
                if [x, y] in fields_threatened:
                    is_threatened[int(not turn)] = True
                    interfere = can_interfere(attackers, [x, y])
                else:
                    is_threatened[int(not turn)] = False
                    interfere = None
                break
            else:
                is_threatened[int(not turn)] = False
                interfere = None

        # check for checkmate
        has_possible_moves = False
        for x, y in numpy.ndindex(grid.shape):
            if grid[x, y] % 2 == turn % 2:
                coords_position = [x, y]
                id = grid[coords_position[0], coords_position[1]]
                possible_moves = get_possible_moves(
                    grid, id, coords_position, [], coords_goal, 0
                )
                if id < 11 and interfere is not None:
                    for mov in possible_moves.copy():
                        if mov not in interfere:
                            possible_moves.remove(mov)
                grid_edited = grid.copy()
                if grid[coords_position[0], coords_position[1]] != 11 + int(not turn):
                    for goal in possible_moves.copy():
                        grid_edited_2 = move(
                            id, coords_position, goal, grid_edited, True
                        )
                        for x, y in numpy.ndindex(grid.shape):
                            if grid[x, y] == 11 + int(not turn):
                                fields_threatened, attackers = get_fields_threatened(
                                    id, grid_edited_2, [x, y], 0
                                )
                                if [x, y] in fields_threatened:
                                    while goal in possible_moves:
                                        possible_moves.remove(goal)
                                break
                if len(possible_moves):
                    has_possible_moves = True
                    break
        if not has_possible_moves:
            if is_threatened[not turn]:
                result = "CHECKMATE"
            else:
                result = "STALEMATE"
        possible_moves = []

    is_threatened[not turn] = False


def create_grid():
    grid = numpy.zeros((8, 8))
    grid[0:8, 6] = 1
    grid[0:8, 1] = 2
    grid[0, 7] = 3
    grid[7, 7] = 3
    grid[0, 0] = 4
    grid[7, 0] = 4
    grid[1, 7] = 5
    grid[6, 7] = 5
    grid[1, 0] = 6
    grid[6, 0] = 6
    grid[2, 7] = 7
    grid[5, 7] = 7
    grid[2, 0] = 8
    grid[5, 0] = 8
    grid[3, 7] = 9
    grid[4, 7] = 11
    grid[3, 0] = 10
    grid[4, 0] = 12
    return grid


def reset():
    global turn, grid, graveyard, possible_moves, last_position, is_threatened, threatened, interfere, castling, castle_moves, result

    turn = 1
    grid = create_grid()
    graveyard = []
    possible_moves = []
    last_position = None
    is_threatened = [False, False]
    threatened = []
    interfere = None
    castling = [True, True, True, True]
    castle_moves = [
        [[None, None], [None, None], [None, None], [None, None]],
        [[None, None], [None, None], [None, None], [None, None]],
    ]
    result = 0


def update():
    global threatened, possible_moves, last_position, result

    data = engine.update(
        grid, possible_moves, turn, graveyard, threatened, is_threatened
    )
    if data[0] is None:
        possible_moves = []
        last_position = None
    else:
        threatened = check_move(*data[:2])
    if result:
        engine.game_end(result)
        data = list(data)
        data[2] = False
    return data[2]
