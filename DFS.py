from Utility import Node
from Algorithm import Algorithm


class DFS(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def recursive_DFS(self, snake, goalstate, currentstate):
        # check if goal state
        if currentstate.equal(goalstate):
            return self.get_path(currentstate)

        # if already visted return
        if currentstate in self.explored_set:
            return None

        self.explored_set.append(currentstate)  # mark visited
        neighbors = self.get_neighbors(currentstate)  # get neighbors

        # for each neighbor
        for neighbor in neighbors:
            if not self.inside_body(snake, neighbor) and not self.outside_boundary(neighbor) and neighbor not in self.explored_set:
                neighbor.parent = currentstate  # mark parent node
                path = self.recursive_DFS(
                    snake, goalstate, neighbor)  # check neighbor
                if path != None:
                    return path  # found path
        return None

    def run_algorithm(self, snake):
        # to avoid looping in the same location
        if len(self.path) != 0:
            # while you have path keep going
            path = self.path.pop()

            if self.inside_body(snake, path):
                self.path = [] # or calculate new path!
            else:
                return path

        # start clean
        self.frontier = []
        self.explored_set = []
        self.path = []

        initialstate, goalstate = self.get_initstate_and_goalstate(snake)

        self.frontier.append(initialstate)

        # return path
        return self.recursive_DFS(snake, goalstate, initialstate)
        
    def estimate_safety(self, snake, currentstate, goalstate):
        # Đánh giá khoảng cách đến thức ăn
        distance_to_fruit = self.calculate_distance(currentstate, snake.get_fruit())

        # Đánh giá khoảng cách đến cơ thể rắn
        min_distance_to_body = min(
            self.calculate_distance(currentstate, body) for body in snake.body[1:]
        )

        # Đánh giá khoảng cách đến biên màn hình
        distance_to_border = min(
            currentstate.x,
            currentstate.y,
            NO_OF_CELLS - 1 - currentstate.x,
            NO_OF_CELLS - 1 - currentstate.y,
        )

        # Tính điểm an toàn tổng thể
        safety_score = (
            some_weight * distance_to_fruit
            + another_weight * min_distance_to_body
            + yet_another_weight * distance_to_border
        )

        # trả về điểm an toàn
        return safety_score

    def calculate_distance(self, point1, point2):
        return abs(point1.x - point2.x) + abs(point1.y - point2.y)