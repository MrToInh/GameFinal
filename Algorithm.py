from abc import ABC, abstractmethod
from Constants import NO_OF_CELLS, BANNER_HEIGHT
from Utility import Node
import math


class Algorithm(ABC):

    def __init__(self, grid):
        self.grid = grid
        self.frontier = []
        self.explored_set = []
        self.path = []
        self.explored_nodes_reverse = []

    def get_initstate_and_goalstate(self, snake):
        return Node(snake.get_x(), snake.get_y()), Node(snake.get_fruit().x, snake.get_fruit().y)

    def manhattan_distance(self, nodeA, nodeB):
        distance_1 = abs(nodeA.x - nodeB.x)
        distance_2 = abs(nodeA.y - nodeB.y)
        return distance_1 + distance_2

    def euclidean_distance(self, nodeA, nodeB):
        distance_1 = nodeA.x - nodeB.x
        distance_2 = nodeA.y - nodeB.y
        return math.sqrt(distance_1**2 + distance_2**2)

    @abstractmethod
    def run_algorithm(self, snake):
        pass

    #Phương thức này xây dựng và trả về đường đi từ nút đích đến nút ban đầu. 
    #Đường đi được lưu trong thuộc tính path.
    def get_path(self, node):
        
        # Nếu trạng thái hiện tại không có trạng thái cha (là trạng thái ban đầu)
        if node.parent is None:
            return node

        # Lặp qua các trạng thái cha để xây dựng đường đi
        while node.parent.parent is not None:
            self.path.append(node)  # Thêm trạng thái vào đường đi
            node = node.parent  # Chuyển sang trạng thái cha

        return node


    #Phương thức kiểm tra xem một nút có nằm trong cơ thể của con rắn hay không.
    def inside_body(self, snake, node):
        for body in snake.body:
            if body.x == node.x and body.y == node.y:
                return True
        return False

    #Phương thức này trả về các nút láng giềng của một nút trên lưới.
    def outside_boundary(self, node):
        if not 0 <= node.x < NO_OF_CELLS:
            return True
        elif not BANNER_HEIGHT <= node.y < NO_OF_CELLS:
            return True
        return False

    def get_neighbors(self, node):
        i = int(node.x)
        j = int(node.y)

        neighbors = []
        # left [i-1, j]
        if i > 0:
            neighbors.append(self.grid[i-1][j])
        # right [i+1, j]
        if i < NO_OF_CELLS - 1:
            neighbors.append(self.grid[i+1][j])
        # top [i, j-1]
        if j > 0:
            neighbors.append(self.grid[i][j-1])    

        # bottom [i, j+1]
        if j < NO_OF_CELLS - 1:
            neighbors.append(self.grid[i][j+1])

        return neighbors
