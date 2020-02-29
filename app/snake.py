import random
from enum import Enum
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from .behaviours import Behaviours


class Moves(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class Snake:

    
    def __init__(self):
        """
        Snake Constructor
        Initializes stateful snake
        """
        self.finder = AStarFinder()
        self.behave = Behaviours()

    def initialize(self, data):
        """
        Initializes stateful snake
        """
        # Get board information
        game_board = data["board"]
        # Determine board dimensions
        self.board_width = game_board["width"]
        self.board_height = game_board["height"]
        self.snake_id = data["you"]["id"]

    def apperance(self):
        color="#ff00ff"
        headType="silly"
        tailType="skinny"
        return color, headType, tailType



    def move(self, data):
        """
        Move the snake to a chosen square
        """
        # update snake status for this turn
        snake_status = self.update_snake_status(data)

        # create a grid representation of the board
        grid = self.build_grid(data)

        # chose a target
        target, path = self.chose_target(data, grid)

        # Determine direction of movement
        direction = self.chose_direction(snake_status["head"], path)
        return direction

    def update_snake_status(self, data):
        """
        Gather information about the snake, including
        head and tail locations as well as health
        """
        snake_status = {
            "head": (0, 0),
            "tail": (0, 0),
            "health": 0
        }
        # Find head
        snake_body = data["you"]["body"]
        my_head = snake_body[0]
        snake_status["head"] = (my_head["x"], my_head["y"])
        # Find tail
        my_tail = snake_body[-1]
        snake_status["tail"] = (my_tail["x"], my_tail["y"])
        # Get the snake's health
        snake_status["health"] = data["you"]["health"]
        return snake_status

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
        if len(path) >= 2:
            # the first element in the list is always the current location, so
            # we take the second element, which represents the first move
            # towards our target
            move = path[1]
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
            # if no path to the target exists (path= [])
            # choose a random move
            direction = random.choice(list(Moves))

        return direction

    def chose_target(self, data, grid):
        """
        Determines the target cell the snake will attempt to move to
        based on the board setup and snake strategy
        RETURNS: a tuple containing the coordinates of the target
        """
        snake_status = self.update_snake_status(data)

        target = None

        snake_size = len(data["you"]["body"])
        if (snake_size < 5 or snake_status["health"] < 50):
            food = data["board"]["food"]
            target, path = self.behave.feed(food, grid, snake_status, self.finder)

        if target is None:
            # find if there is a path to the tail
            target, path = self.behave.chase_tail(grid, snake_status, self.finder)

        if target is None:
            target, path = self.behave.move_to_neighbour(grid, snake_status, self.finder)

        if target is None:
            # If all fails, the last resort is to try to chase the tail anyway
            # and take the risk of colliding with it.
            tail_path, length = self.behave.head_to_tail(snake_status, grid, self.finder)
            path = tail_path[0]

        return target, path
