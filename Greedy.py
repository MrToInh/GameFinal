from Algorithm import Algorithm

class Greedy(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def run_algorithm(self, snake):
        # clear everything
        self.frontier = []
        self.explored_set = []
        self.path = []

        initialstate, goalstate = self.get_initstate_and_goalstate(snake)

        # open list
        self.frontier.append(initialstate)

        # while we have states in open list
        while len(self.frontier) > 0:
            # get node with lowest heuristic h(n)
            lowest_index = 0
            for i in range(len(self.frontier)):
                if self.manhattan_distance(self.frontier[i], goalstate) < self.manhattan_distance(self.frontier[lowest_index], goalstate):
                    lowest_index = i

            lowest_node = self.frontier.pop(lowest_index)

            # check if its goal state
            if lowest_node.equal(goalstate):
                return self.get_path(lowest_node)

            self.explored_set.append(lowest_node)  # mark visited
            neighbors = self.get_neighbors(lowest_node)  # get neighbors

            # for each neighbor
            for neighbor in neighbors:
                # check if path inside snake, outside boundary, or already visited
                if self.inside_body(snake, neighbor) or self.outside_boundary(neighbor) or neighbor in self.explored_set:
                    continue  # skip this path

                if neighbor not in self.frontier:  # first time visiting
                    neighbor.parent = lowest_node
                    self.frontier.append(neighbor)


        # Trường hợp không tìm thấy đường đi
        return None
