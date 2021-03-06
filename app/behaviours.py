class Behaviours:

    def feed(self, food, grid, snake_status, finder):
        """
        Selects the closes food to the snake. The selected food
        needs to be reachable by the snake, which means that a
        possible path between the head of the snake and the food
        needs to exist.
        RETURNS: Coordinate tuple to the closest snake, or None if
        no food is reachable
        """
        head = snake_status["head"]
        head_loc = grid.node(head[0], head[1])
        target = None
        food_path = []

        # sort the food by proximity to the snake
        closer_food = sorted(food, key=lambda apple:
                             abs(head[0] - apple['x']) + abs(head[1] - apple['y']))
        # chose the closest reachable apple
        for chosen_apple in closer_food:
            apple = (chosen_apple["x"], chosen_apple["y"])
            apple_loc = grid.node(apple[0], apple[1])

            # verify that a path to the chosen apple exists
            path = finder.find_path(head_loc, apple_loc, grid)
            grid.cleanup()

            if len(path[0]) >= 2:
                danger = self.assess_danger(grid, apple_loc, snake_status, finder)
                if danger <= 2:
                    target = apple
                    food_path = path[0]
                    break

        return target, food_path

    def chase_tail(self, grid, snake_status, finder):
        """
        Returns the coordinate to the snake's tail.
        If the tail is in the immediate neighbour, there is a risk that if the
        snake grows and the tail will remain on its square, we may move right into
        it and collide. In this case we return None to indicate that we should not
        chase the tail
        RETURNS: Coordinate tuple to the snake's tail, or None if
        tail is not reachable or it is in an immediate neighbour.
        """
        head = snake_status["head"]
        head_loc = grid.node(head[0], head[1])

        # find if there is a path to the tail
        path, path_length = self.path_to_tail(head_loc, snake_status, grid, finder)

        target = None

        # if the tail is at least one square away from the head, then
        # proceed with the move
        if path_length >= 2:
            next_move = path[0][1]
            next_node = grid.node(next_move[0], next_move[1])
            danger = self.assess_danger(grid, next_node, snake_status, finder)
            if danger <= 2:
                target = snake_status["tail"]

        return target, path[0]

    def move_to_neighbour(self, grid, snake_status, finder):
        """
        Returns the coordinate to the first neighbour square where the snake can
        move into safely
        RETURNS: Coordinate tuple to a walkable neighbour, or None if
        no neighbour is walkable.
        """
        head = snake_status["head"]
        head_loc = grid.node(head[0], head[1])

        target = None
        path = []

        # Find the first walkable neighbour
        neighbours = finder.find_neighbors(grid, head_loc, diagonal_movement=None)
        if len(neighbours) > 0:
            danger_sort = sorted(neighbours, key=lambda node: self.assess_danger(grid, node, snake_status, finder))
            adjacent = danger_sort[0]
            target = (adjacent.x, adjacent.y)
            path_found = finder.find_path(head_loc, adjacent, grid)
            grid.cleanup()
            if len(path_found) > 0:
                path = path_found[0]

        return target, path

    def assess_danger(self, grid, node, snake_status, finder):
        neighbours = finder.find_neighbors(grid, node, diagonal_movement=None)
        danger_score = 4 - len(neighbours)

        path, length = self.path_to_tail(node, snake_status, grid, finder)
        if (length <= 1):
            danger_score = danger_score + 100
        return danger_score

    def path_to_tail(self, origin, snake_status, grid, finder):
        tail = snake_status["tail"]
        tail_loc = grid.node(tail[0], tail[1])

        tail_loc.walkable = True
        tail_loc.weight = 1

        path = finder.find_path(origin, tail_loc, grid)
        grid.cleanup()

        tail_loc.walkable = False
        tail_loc.weight = 0

        return path, len(path[0])

    def head_to_tail(self, snake_status, grid, finder):

        head = snake_status["head"]
        head_loc = grid.node(head[0], head[1])

        path, length = self.path_to_tail(head_loc, snake_status, grid, finder)

        return path, length
