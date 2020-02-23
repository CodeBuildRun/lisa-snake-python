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
                danger = self.assess_danger(grid, apple_loc, finder)
                if danger <= 1:
                    target = apple
                    break

        return target

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
        tail = snake_status["tail"]
        tail_loc = grid.node(tail[0], tail[1])

        head = snake_status["head"]
        head_loc = grid.node(head[0], head[1])

        # find if there is a path to the tail
        path = finder.find_path(head_loc, tail_loc, grid)
        grid.cleanup()

        target = None

        # if the tail is at least one square away from the head, then
        # proceed with the move
        if len(path[0]) >= 2:
            next_move = path[0][1]
            next_node = grid.node(next_move[0], next_move[1])
            if self.assess_danger(grid, next_node, finder) < 1:
                target = tail

        return target

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

        # Find the first walkable neighbour
        neighbours = finder.find_neighbors(grid, head_loc, diagonal_movement=None)
        if len(neighbours) > 0:
            danger_sort = sorted(neighbours, key=lambda node: self.assess_danger(grid, node, finder))
            adjacent = danger_sort[0]
            target = (adjacent.x, adjacent.y)

        return target

    def assess_danger(self, grid, node, finder):
        neighbours = finder.find_neighbors(grid, node, diagonal_movement=None)
        danger_score = 4 - len(neighbours)
        return danger_score
