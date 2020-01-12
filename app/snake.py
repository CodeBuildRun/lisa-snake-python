import random


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

        directions = ['up', 'down', 'left', 'right']
        # direction = random.choice(directions)
        # Make a list of all the bad coordinates and try to avoid them
        height = data["board"]["height"]
        width = data["board"]["width"]
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
        for snake in data["board"]["snakes"]:
            for body in snake["body"]:
                bad = (body["x"], body["y"])
                bad_coords.append(bad)
        possible_moves = []

        # get coordinates of my snake head
        my_head = data["you"]["body"][0]

        # up
        coord = (my_head["x"], my_head["y"]-1)
        if coord not in bad_coords:
            possible_moves.append("up")
        # down
        coord = (my_head["x"], my_head["y"]+1)
        if coord not in bad_coords:
            possible_moves.append("down")
        # left
        coord = (my_head["x"]-1, my_head["y"])
        if coord not in bad_coords:
            possible_moves.append("left")
        # right
        coord = (my_head["x"]+1, my_head["y"])
        if coord not in bad_coords:
            possible_moves.append("right")

        # possible moves
        if len(possible_moves) > 0:
            direction = random.choice(possible_moves)
        else:
            direction = random.choice(directions)

        return direction
