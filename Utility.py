from Constants import NO_OF_CELLS


class Node:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.h = 0
        self.g = 0
        self.f = 1000000
        self.parent = None
        self.is_obstacle = False  # Add this attribute


    def print(self):
        print(f"x: {self.x} y: {self.y}")

    def equal(self, b):
        return self.x == b.x and self.y == b.y



class Grid:
    def __init__(self):
        self.grid = []

        for i in range(NO_OF_CELLS):
            col = []
            for j in range(NO_OF_CELLS):
                col.append(Node(i, j))
            self.grid.append(col)
        #  # Mark certain nodes as obstacles
        # self.grid[1][1].is_obstacle = True
        # self.grid[2][2].is_obstacle = True
        # Add more obstacle nodes as needed

        for j in range(15,int(NO_OF_CELLS-2)):
            self.grid[3][j].is_obstacle = True
        for i in range(3,6):
            self.grid[i][5].is_obstacle = True