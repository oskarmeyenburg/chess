import math
import time
import sys
import os

import numpy
import pygame

board_size = 50 * 8  # has to be divisible by 8; 40*8
board_size4 = int(board_size / 4)
board_size8 = int(board_size / 8)
game_fps = 50

# set up pygame
pygame.init()
window = pygame.display.set_mode((board_size * 1.5, board_size))
board = pygame.Surface((board_size, board_size))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

# import font
font_s = pygame.font.SysFont(None, int(board_size / 16))
font_m = pygame.font.SysFont(None, int(board_size / 12))
font_l = pygame.font.SysFont(None, int(board_size / 5))

# set up chess board pattern
bg = pygame.Surface((board_size, board_size))
bg.fill((75, 75, 75))
for x in range(8):
    for y in range(8):
        if (x + y) % 2 == 0:
            pygame.draw.rect(
                bg,
                (150, 150, 150),
                (x * board_size8, y * board_size8, board_size8, board_size8),
            )

# set up green field
green = pygame.Surface((math.ceil(board_size8), math.ceil(board_size8)))
green.fill((0, 255, 0))
green.set_alpha(100)

# set up red field
red = pygame.Surface((math.ceil(board_size8), math.ceil(board_size8)))
red.fill((255, 0, 0))
red.set_alpha(100)

# set up turn gradient
gradient = pygame.Surface((6, 4))
pygame.draw.rect(gradient, (50, 50, 50), (0, 0, 6, 2))
pygame.draw.rect(gradient, (200, 200, 200), (0, 2, 6, 2))
gradient = pygame.transform.smoothscale(
    gradient, (int(board_size * 2), int(board_size * 2.5))
)

# extract piece from chess_pieces.png
project_path = os.path.dirname(os.path.split(__file__)[0])
image_path = os.path.join(project_path, "assets", "resources", "chess_pieces.png")
chess_pieces = pygame.image.load(image_path)


def load_piece(x, y):
    img = pygame.Surface((200, 200), pygame.SRCALPHA)
    img.blit(chess_pieces, (0, 0), (x * 200, y * 200, 200, 200))
    img = pygame.transform.scale(img, (board_size8, board_size8))
    return img


# empty        = 0
# white pawn   = 1
# black pawn   = 2
# white rook   = 3
# black rook   = 4
# white knight = 5
# black knight = 6
# white bishop = 7
# black bishop = 8
# white queen  = 9
# black queen  = 10
# white king   = 11
# black king   = 12

piece = {
    1: load_piece(5, 0),
    2: load_piece(5, 1),
    3: load_piece(4, 0),
    4: load_piece(4, 1),
    5: load_piece(3, 0),
    6: load_piece(3, 1),
    7: load_piece(2, 0),
    8: load_piece(2, 1),
    9: load_piece(1, 0),
    10: load_piece(1, 1),
    11: load_piece(0, 0),
    12: load_piece(0, 1),
}

selected_piece = None
selected_goal = None
grab = (0, 0)
pygame.display.set_icon(piece[1])
gradient_pos = int(1 * -board_size)


def get_mouse_pos():
    """
    Get mouse position algined with board on screen.
    """
    pos = pygame.mouse.get_pos()
    return (pos[0] - board_size * 0.25, pos[1])


def valid_position(position):
    """
    Check whether position is on chess board.
    """
    return 0 <= position[0] <= 7 and 0 <= position[1] <= 7


def game_end(result):
    to_menu = False
    add = int(time.time() / 2) % 2 * board_size8
    while not to_menu:
        window.fill((75, 75, 75))
        for x in range(12):
            for y in range(8):
                if (x + y) % 2:
                    pygame.draw.rect(
                        window,
                        (150, 150, 150),
                        (
                            int(x * board_size8),
                            int(y * board_size8),
                            int(board_size8),
                            int(board_size8),
                        ),
                    )
        for location in (
            (11, 0, 6),
            (4, 1, 2),
            (5, 0, 4),
            (1, 2, 5),
            (6, 2, 0),
            (9, 8, 7),
            (6, 11, 6),
            (8, 11, 4),
            (12, 11, 3),
            (3, 10, 0),
        ):
            window.blit(
                piece[location[0]],
                (location[1] * board_size8, location[2] * board_size8),
            )
        mouse_pos = pygame.mouse.get_pos()
        if pygame.Rect(
            int(4 * board_size8),
            int(3 * board_size8),
            int(board_size / 2),
            int(board_size8),
        ).collidepoint(mouse_pos):
            for x in range(4):
                window.blit(green, (int((x + 4) * board_size8), int(3 * board_size8)))
            if True in pygame.mouse.get_pressed():
                to_menu = True

        add = int((add + int(time.time() / 2) % 2 * board_size8 * 2) / 3)
        for char in enumerate(result):
            image = font_l.render(char[1], True, (0, 0, 0))
            center = image.get_rect().center
            window.blit(
                image,
                (
                    int(
                        board_size * 0.75
                        - image.get_width() / 2
                        + board_size / 12
                        - center[0] / 2
                        + (char[0] - 5) * board_size8
                        + add
                    ),
                    int(board_size * 0.25 - board_size / 12 - center[1] / 2),
                ),
            )
        for char in enumerate("MENU"):
            image = font_l.render(char[1], True, (0, 0, 0))
            center = image.get_rect().center
            window.blit(
                image,
                (
                    int(
                        board_size * 0.75
                        - image.get_width() / 2
                        + board_size / 12
                        - center[0] / 2
                        + (char[0] - 2) * board_size8
                    ),
                    int(board_size * 0.5 - board_size / 12 - center[1] / 2),
                ),
            )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(game_fps)
    time.sleep(1)


def menu():
    add = int(time.time() / 2) % 2 * board_size8
    play = False
    while not play:
        mouse_pos = pygame.mouse.get_pos()
        window.fill((75, 75, 75))
        for x in range(12):
            for y in range(8):
                if (x + y) % 2:
                    pygame.draw.rect(
                        window,
                        (150, 150, 150),
                        (
                            int(x * board_size8),
                            int(y * board_size8),
                            int(board_size8),
                            int(board_size8),
                        ),
                    )
        for location in (
            (11, 0, 6),
            (4, 1, 2),
            (5, 0, 4),
            (1, 2, 5),
            (6, 2, 0),
            (9, 8, 7),
            (6, 11, 6),
            (8, 11, 4),
            (12, 11, 3),
            (3, 10, 1),
        ):
            window.blit(
                piece[location[0]],
                (location[1] * board_size8, location[2] * board_size8),
            )

        if pygame.Rect(
            int(4 * board_size8),
            int(3 * board_size8),
            int(board_size / 2),
            int(board_size8),
        ).collidepoint(mouse_pos):
            for x in range(4):
                window.blit(green, (int((x + 4) * board_size8), int(3 * board_size8)))
            if True in pygame.mouse.get_pressed():
                play = True
        add = int((add + int(time.time() / 2) % 2 * board_size8 * 2) / 3)
        for char in enumerate("CHESS"):
            image = font_l.render(char[1], True, (0, 0, 0))
            center = image.get_rect().center
            window.blit(
                image,
                (
                    int(
                        board_size * 0.75
                        - image.get_width() / 2
                        + board_size / 12
                        - center[0] / 2
                        + (char[0] - 3) * board_size8
                        + add
                    ),
                    int(board_size * 0.25 - board_size / 12 - center[1] / 2),
                ),
            )
        for char in enumerate("PLAY"):
            image = font_l.render(char[1], True, (0, 0, 0))
            center = image.get_rect().center
            window.blit(
                image,
                (
                    int(
                        board_size * 0.75
                        - image.get_width() / 2
                        + board_size / 12
                        - center[0] / 2
                        + (char[0] - 2) * board_size8
                    ),
                    int(board_size * 0.5 - board_size / 12 - center[1] / 2),
                ),
            )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(game_fps)


def get_pawn_promotion(turn):
    global gradient_pos

    selected = False
    while not selected:
        gradient_pos = int((gradient_pos * 99 + turn * -board_size) / 100)
        window.blit(
            gradient, (0, gradient_pos), (0, 0, board_size * 0.25, board_size * 2.5)
        )
        window.blit(
            gradient,
            (board_size * 1.25, gradient_pos),
            (0, 0, board_size * 0.25, board_size * 2.5),
        )
        window.blit(board, (board_size * 0.25, 0))
        fps = font_m.render(str(int(clock.get_fps())), True, (50, 50, 50))
        window.blit(
            fps, (int(board_size * 1.27), int((board_size - fps.get_height()) * 0.98))
        )
        menu = font_m.render("menu", True, (50, 50, 50))
        window.blit(
            menu, (int(board_size * 0.02), int((board_size - menu.get_height()) * 0.98))
        )
        mouse_pos = pygame.mouse.get_pos()
        for i in range(2, 10):
            if turn != i % 2:
                x = int((i + 1) % 2 * board_size * 1.25)
                y = int(
                    (i - (i) % 2 - 2) / 2 * board_size8
                    + board_size / 64 * (i - (i) % 2 - 1)
                )
                mask = pygame.mask.from_surface(piece[i + 1])
                if pygame.Rect(x, y, *piece[i + 1].get_size()).collidepoint(
                    mouse_pos
                ) and mask.get_at((mouse_pos[0] - x, mouse_pos[1] - y)):
                    if True in pygame.mouse.get_pressed():
                        selected = i + 1
                    for point in mask.outline():
                        pygame.draw.circle(
                            window, (0, 200, 0), (x + point[0], y + point[1]), 3
                        )
                else:
                    for point in mask.outline():
                        pygame.draw.circle(
                            window, (150, 200, 150), (x + point[0], y + point[1]), 3
                        )
                window.blit(piece[i + 1], (x, y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(game_fps)
    return selected


# update every tick
def update(grid, possible_moves, turn, graveyard, threatened, is_threatened):
    global selected_piece, selected_goal, grab, gradient_pos

    if selected_goal is not None:
        selected_piece = None
        selected_goal = None
    mouse_pos = get_mouse_pos()
    play = True

    # draw on board
    board.blit(bg, (0, 0))
    for possible_move in possible_moves:
        board.blit(
            green,
            (int(possible_move[0] * board_size8), int(possible_move[1] * board_size8)),
        )
    if threatened is not None:
        for possible_move in threatened:
            board.blit(
                red,
                (
                    int(possible_move[0] * board_size8),
                    int(possible_move[1] * board_size8),
                ),
            )
    for x, y in numpy.ndindex(grid.shape):
        if grid[x, y] >= 11 and is_threatened[int(grid[x, y]) - 11]:
            board.blit(red, (int(x * board_size8), int(y * board_size8)))
        if grid[x, y] != 0:
            if (x, y) != selected_piece:
                board.blit(
                    piece[grid[x, y]], (int(x * board_size8), int(y * board_size8))
                )

    # get events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if selected_piece is None:
                selected_piece = (
                    int(mouse_pos[0] / board_size * 8),
                    int(mouse_pos[1] / board_size * 8),
                )
                grab = mouse_pos
            else:
                selected_goal = (
                    int(mouse_pos[0] / board_size * 8),
                    int(mouse_pos[1] / board_size * 8),
                )
            if pygame.Rect(0, board_size8 * 7, board_size4, board_size8).collidepoint(
                pygame.mouse.get_pos()
            ):
                play = False
        if event.type == pygame.MOUSEBUTTONUP:
            if selected_piece != (
                int(mouse_pos[0] / board_size * 8),
                int(mouse_pos[1] / board_size * 8),
            ):
                selected_goal = (
                    int(mouse_pos[0] / board_size * 8),
                    int(mouse_pos[1] / board_size * 8),
                )
    if selected_piece is not None and valid_position(selected_piece) and (
        grid[selected_piece[0], selected_piece[1]] == 0
        or grid[selected_piece[0], selected_piece[1]] % 2 != turn
    ):
        selected_piece = None

    # draw to window
    gradient_pos = int((gradient_pos * 99 + turn * -board_size) / 100)
    window.blit(gradient, (0, gradient_pos))
    window.blit(board, (board_size * 0.25, 0))
    if (
        selected_piece is not None
        and valid_position(selected_piece)
        and grid[selected_piece[0], selected_piece[1]] % 2 == turn
    ):
        pygame.draw.rect(
            window,
            (0, 50, 0),
            (
                int(selected_piece[0] * board_size8 - 3 + board_size4),
                int(selected_piece[1] * board_size8 - 3),
                int(board_size8 + 6),
                int(board_size8 + 6),
            ),
            6,
            6,
        )
    if (
        selected_piece is not None
        and valid_position(selected_piece)
        and grid[selected_piece[0], selected_piece[1]] != 0
    ):
        window.blit(
            piece[grid[selected_piece[0], selected_piece[1]]],
            (
                int(
                    selected_piece[0] * board_size8
                    - grab[0]
                    + mouse_pos[0]
                    + board_size4
                ),
                int(selected_piece[1] * board_size8 - grab[1] + mouse_pos[1]),
            ),
        )
    fps = font_m.render(str(int(clock.get_fps())), True, (50, 50, 50))
    window.blit(
        fps, (int(board_size * 1.27), int((board_size - fps.get_height()) * 0.98))
    )
    menu = font_m.render("menu", True, (50, 50, 50))
    window.blit(
        menu, (int(board_size * 0.02), int((board_size - menu.get_height()) * 0.98))
    )

    # draw grave yard
    for i in range(12):
        count = graveyard.count(i + 1)
        if count:
            x = int((i + 1) % 2 * board_size * 1.25)
            y = int(
                (i - (i) % 2) / 2 * board_size8 + board_size / 64 * (i - (i) % 2 + 1)
            )
            window.blit(piece[i + 1], (x, y))
            if count - 1:
                count = font_m.render(
                    str(count),
                    False,
                    (((turn - 1) * -255), ((turn - 1) * -255), ((turn - 1) * -255)),
                    (255, 0, 0),
                )
                count.set_colorkey((255, 0, 0))
                window.blit(count, (x + board_size / 9, y + board_size / 9))

    # update window
    pygame.display.update()
    clock.tick(game_fps)

    # return data
    if (selected_piece is not None) and (
        selected_piece[0] < 0
        or selected_piece[0] > 7
        or selected_piece[1] < 0
        or selected_piece[1] > 7
    ):
        selected_piece = None
    if (selected_piece is not None) and (
        grid[selected_piece[0], selected_piece[1]] == 0
        or grid[selected_piece[0], selected_piece[1]] % 2 != turn
    ):
        selected_piece = None
    return selected_piece, selected_goal, play
