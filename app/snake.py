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
        Snake Constructor
        Initializes stateful snake
        """

    def initialize(self, data):
        """
        Initializes stateful snake
        """
        # Get board information
        game_board = data["board"]
        # Determine board dimensions
        self.board_width = game_board["width"]
        self.board_height = game_board["height"]

        return Snake.snake_color

    def move(self, data):
        """
        Move the snake to a chosen square
        """
        # print(json.dumps(data))

        # Get the board's current state
        game_board = data["board"]

        # Make a list of all the board locations to avoid
        bad_coords = self.get_bad_coords(game_board)

        # get coordinates of my snake head
        my_head = self.get_snake_head(data)

        # Determine direction of movement
        direction = self.chose_direction(my_head, bad_coords)
        return direction

    def get_snake_head(self, data):
        """
        Get coordinates of the snake's head
        """
        my_head_json = data["you"]["body"][0]
        my_head = (my_head_json["x"], my_head_json["y"])
        return my_head

    def get_bad_coords(self, game_board):
        """
        Make a list of all the coordinates to avoid
        """
        bad_coords = []

        # Bad coordinates that my snake needs to avoid
        # 1. snake bodies on the board
        for snake in game_board["snakes"]:
            for body in snake["body"]:
                bad = (body["x"], body["y"])
                bad_coords.append(bad)
        return bad_coords

    def is_coord_on_board(self, coord):
        """
        Determines if a given coordinate is on the board
        RETURNS: True if coordinate is on the board, False otherwise
        """
        on_board = False

        if (coord[0] >= 0 and coord[0] < self.board_width) and \
           (coord[1] >= 0 and coord[1] < self.board_height):
            on_board = True

        return on_board

    def chose_direction(self, my_head, bad_coords):
        """
        Choses a direction to move based on the position of the snake's head
        and a list of squares to avoid
        Inputs:
            my_head   : A tuple including the coordinates of the snake's head
            bad_coords: A list of squares in the board that should be avoided
        Returns:
            direction : The chosen direction to move [UP, DOWN, LEFT, RIGHT]
        """
        # Create a list that will contain all possible moves
        possible_moves = []

        # Determine direction of movement
        # up
        coord = (my_head[0], my_head[1] - 1)
        if (self.is_coord_on_board(coord)) and (coord not in bad_coords):
            possible_moves.append(Moves.UP)
        # down
        coord = (my_head[0], my_head[1] + 1)
        if (self.is_coord_on_board(coord)) and (coord not in bad_coords):
            possible_moves.append(Moves.DOWN)
        # left
        coord = (my_head[0] - 1, my_head[1])
        if (self.is_coord_on_board(coord)) and (coord not in bad_coords):
            possible_moves.append(Moves.LEFT)
        # right
        coord = (my_head[0] + 1, my_head[1])
        if (self.is_coord_on_board(coord)) and (coord not in bad_coords):
            possible_moves.append(Moves.RIGHT)

        # possible moves
        if len(possible_moves) > 0:
            direction = random.choice(possible_moves)
        else:
            direction = random.choice(list(Moves))

        return direction
