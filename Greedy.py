from Algorithm import Algorithm

class Greedy(Algorithm):
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
            # get node with the lowest h(n)
            self.frontier.sort(key=lambda node: node.h)
            current_node = self.frontier.pop(0)

            # check if it's the goal state
            if current_node.equal(goal_state):
                return self.get_path(current_node)

            self.explored_set.append(current_node)  # mark visited

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

                # calculate heuristic value h(n)
                neighbor.h = self.manhattan_distance(goal_state, neighbor)

                # add neighbor to the priority queue
                self.frontier.append(neighbor)
                neighbor.parent = current_node

        return None
