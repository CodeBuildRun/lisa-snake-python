import json
import random
from enum import Enum


class Moves(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class Snake:

    snake_color = "#00FF00"

    def __init__(self):
        """
        Snake Constructor.
        Initializes stateful snake
        """

    def color(self):
        return Snake.snake_color

    def move(self, data):

        print(json.dumps(data))

        # Get the board's current state
        game_board = data["board"]
        # get coordinates of my snake head
        my_head = data["you"]["body"][0]
        my_head_x = my_head["x"]
        my_head_y = my_head["y"]

        # Make a list of all the bad coordinates and try to avoid them
        height = game_board["height"]
        width = game_board["width"]
        bad_coords = []

        # Bad coordinates that my snake needs to avoid
        # 1. above and below the board
        for x in range(width):
            bad = (x, -1)
            bad_coords.append(bad)
            bad = (x, height)
            bad_coords.append(bad)

        # 2. left and right to the board
        for y in range(height):
            bad = (-1, y)
            bad_coords.append(bad)
            bad = (width, y)
            bad_coords.append(bad)

        # 3. snake bodies on the board
        for snake in game_board["snakes"]:
            for body in snake["body"]:
                bad = (body["x"], body["y"])
                bad_coords.append(bad)

        possible_moves = []

        # Determine direction of movement
        # up
        coord = (my_head_x, my_head_y - 1)
        if coord not in bad_coords:
            possible_moves.append(Moves.UP)
        # down
        coord = (my_head_x, my_head_y + 1)
        if coord not in bad_coords:
            possible_moves.append(Moves.DOWN)
        # left
        coord = (my_head_x - 1, my_head_y)
        if coord not in bad_coords:
            possible_moves.append(Moves.LEFT)
        # right
        coord = (my_head_x + 1, my_head_y)
        if coord not in bad_coords:
            possible_moves.append(Moves.RIGHT)

        # possible moves
        if len(possible_moves) > 0:
            direction = random.choice(possible_moves)
        else:
            direction = random.choice(list(Moves))

        return direction
