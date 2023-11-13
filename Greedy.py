from Algorithm import Algorithm
from collections import deque

class Greedy(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def run_algorithm(self, snake):
        # clear everything
        self.frontier = deque([])
        self.path = []

        initialstate, goalstate = self.get_initstate_and_goalstate(snake)

        # open list
        self.frontier.append(initialstate)

        # while we have states in open list
        while len(self.frontier) > 0:
            # get the state with the minimum heuristic value (greedy choice)
            current_state = min(self.frontier, key=lambda x: self.manhattan_distance(x, goalstate))

            # check if it's the goal state
            if current_state.equal(goalstate):
                return self.get_path(current_state)

            self.frontier.remove(current_state)  # mark visited

            neighbors = self.get_neighbors(current_state)  # get neighbors

            # for each neighbor
            for neighbor in neighbors:
                # check if path inside snake, outside boundary, or already visited
                if self.inside_body(snake, neighbor) or self.outside_boundary(neighbor) or neighbor in self.frontier:
                    continue  # skip this path

                neighbor.h = self.manhattan_distance(goalstate, neighbor)
                self.frontier.append(neighbor)

        return None