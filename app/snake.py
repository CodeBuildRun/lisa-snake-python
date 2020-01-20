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
        # create a grid representation of the board
        grid = self.build_grid(data)

        # get coordinates of my snake head
        my_head = self.get_snake_head(data)
        start_loc = grid.node(my_head[0], my_head[1])

        # chose a target
        target = self.chose_target(data)
        end_loc = grid.node(target[0], target[1])

        # find a path to the target
        path = self.finder.find_path(start_loc, end_loc, grid)
        print(path)

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

    def get_snake_tail(self, data):
        """
        Get coordinates of the snake's tail
        """
        my_tail_json = data["you"]["body"][-1]
        my_tail = (my_tail_json["x"], my_tail_json["y"])
        return my_tail

    def get_snake_health(self, data):
        """
        Get coordinates of the snake's tail
        """
        my_health = data["you"]["health"]
        return my_health

    def set_bad_coords(self, data, matrix):
        """
        Mark cells in the matrix that the snake needs to avoid
        """
        # Get the board's current state
        game_board = data["board"]

        # TODO: For enemies snake heads, invalidate squares in the
        # head's immediate neighbourhood. This prevent us from moving to
        # the same square the enemy snake choses to move to.
        for snake in game_board["snakes"]:
            for body_part in snake["body"]:
                matrix[body_part["y"]][body_part["x"]] = 0

        tail = self.get_snake_tail(data)
        matrix[tail[1]][tail[0]] = 1

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

    def build_grid(self, data):
        """
        Builds a Grid representation of the board to be processed
        by the pathfinding algorithm
        RETURNS: an instance of Grid containing a 2D representation
        of the board
        """
        # represent the board in a matrix
        board_matrix = [[1 for _ in range(self.board_height)]
                        for _ in range(self.board_width)]
        # Populate the game board with cells to avoid
        self.set_bad_coords(data, board_matrix)

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
            elif vector == (-1, 0):
                direction = Moves.LEFT
            else:
                direction = random.choice(list(Moves))
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
        # chose an apple
        if data["turn"] < 10 or self.get_snake_health(data) < 50:
            food = data["board"]["food"]
            apple = food[0]
            target = (apple["x"], apple["y"])
        else:
            target = self.get_snake_tail(data)

        return target
