from Algorithm import Algorithm


class A_STAR(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def run_algorithm(self, snake):
        # clear everything
        self.frontier = []
        self.explored_set = []
        self.path = []

        initial_state, goal_state = self.get_initstate_and_goalstate(snake)

        # open list using a regular list
        self.frontier.append(initial_state)

        # while we have states in the open list
        while self.frontier:
            # get node with the lowest f(n)
            current_node = min(self.frontier, key=lambda node: node.f)

            # check if it's the goal state
            if current_node.equal(goal_state):
                return self.get_path(current_node)

            self.explored_set.append(current_node)  # mark visited
            self.frontier.remove(current_node)

            neighbors = self.get_neighbors(current_node)  # get neighbors

            # for each neighbor
            for neighbor in neighbors:
                # check if the path is inside the snake, outside the boundary, or already visited
                if (
                    self.inside_body(snake, neighbor)
                    or self.outside_boundary(neighbor)
                    or neighbor in self.explored_set
                ):
                    continue  # skip this path

                g = current_node.g + 1
                h = self.manhattan_distance(goal_state, neighbor)

                # calculate total cost f(n) = g(n) + h(n)
                f = g + h

                best = False  # assuming neighbor path is better

                if neighbor not in self.frontier:
                    self.frontier.append(neighbor)
                    best = True
                elif f < neighbor.f:
                    best = True

                if best:
                    neighbor.parent = current_node
                    neighbor.g = g
                    neighbor.h = h
                    neighbor.f = f

        return None
