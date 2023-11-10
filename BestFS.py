# BestFS.py

from Algorithm import Algorithm
from Utility import Node

from queue import Queue

class BestFirstSearch(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def run_algorithm(self, snake):
        self.frontier = Queue()  # Use a simple queue instead of a priority queue
        self.explored_set = []
        self.path = []

        initialstate, goalstate = self.get_initstate_and_goalstate(snake)

        self.frontier.put(initialstate)

        while not self.frontier.empty():
            current_node = self.frontier.get()

            if current_node in self.explored_set:
                continue

            self.explored_set.append(current_node)

            if current_node.equal(goalstate):
                return self.get_path(current_node)

            neighbors = self.get_neighbors(current_node)

            for neighbor in neighbors:
                if self.inside_body(snake, neighbor) or self.outside_boundary(neighbor):
                    continue

                if neighbor not in self.explored_set:
                    neighbor.parent = current_node
                    self.frontier.put(neighbor)

        return None
