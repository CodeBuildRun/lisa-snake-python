import json
import random
from enum import Enum
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


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
        self.finder = AStarFinder()

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
        # create a grid representation of the board
        grid = self.build_grid(game_board)

        # get coordinates of my snake head
        my_head = self.get_snake_head(data)
        start_loc = grid.node(my_head[0], my_head[1])

        # chose a target
        for tries in range(4):
            target = self.chose_target(data)
            end_loc = grid.node(target[0], target[1])
            print(target)

            # find a path to the target
            path = self.finder.find_path(start_loc, end_loc, grid)
            if len(path[0]) >= 2:
                break
            else:
                print("No PATH")

        # Determine direction of movement
        direction = self.chose_direction(my_head, path)
        return direction

    def get_snake_head(self, data):
        """
        Get coordinates of the snake's head
        """
        my_head_json = data["you"]["body"][0]
        my_head = (my_head_json["x"], my_head_json["y"])
        return my_head

    def set_bad_coords(self, game_board, matrix):
        """
        Mark cells in the matrix that the snake needs to avoid
        """
        for snake in game_board["snakes"]:
            for body_part in snake["body"]:
                matrix[body_part["y"]][body_part["x"]] = 0

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

    def build_grid(self, game_board):
        """
        Builds a Grid representation of the board to be processed
        by the pathfinding algorithm
        RETURNS: an instance of Grid containing a 2D representation
        of the board
        """
        # represent the board in a matrix
        board_matrix = [[1 for y in range(self.board_height)]
                        for x in range(self.board_width)]
        # Populate the game board with cells to avoid
        self.set_bad_coords(game_board, board_matrix)

        return Grid(matrix=board_matrix)

    def chose_direction(self, start_loc, path):
        """
        Determines the direction the snake should move based on the path found
        RETURNS: a direction in Snake.Moves enumeration
        """
        # Check that the path has more than one step so we know we have not yet
        # arrived to the destination. A path with only one step indicates that
        # we are already located on the target destination
        if len(path[0]) >= 2:
            # the first element in the list is always the current location, so
            # we take the second element, which represents the first move
            # towards our target
            move = path[0][1]
            vector = (move[0] - start_loc[0], move[1] - start_loc[1])

            if vector == (0, -1):
                direction = Moves.UP
            elif vector == (0, 1):
                direction = Moves.DOWN
            elif vector == (1, 0):
                direction = Moves.RIGHT
            else:
                direction = Moves.LEFT
        else:
            # TODO: Check the case when the target location is occupied
            # by a snake. In this case, the path will be empty
            # returning a random move for now
            direction = random.choice(list(Moves))

        return direction

    def chose_target(self, data):
        """
        Determines the target cell the snake will attempt to move to
        based on the board setup and snake strategy
        RETURNS: a tuple containing the coordinates of the target
        """
        return random.choice([(14, 14), (0, 0), (0, 14), (14, 0)])
