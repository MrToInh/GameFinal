from Snake import Snake
from Constants import NO_OF_CELLS, BANNER_HEIGHT
from Utility import Grid
from DFS import DFS
from BFS import BFS
from UCS import UCS
from A_STAR import A_STAR
from Greedy import Greedy
from BestFS import BestFirstSearch
class GameController:

    def __init__(self):
        self.snake = None
        self.snakes = []
        self.score = 0
        self.steps = 0
        self.end = False
        self.grid = Grid().grid
        self.algo = None
        self.model_loaded = False

    def reset(self):
        self.end = False
        if self.snake:
            self.snake.reset()
            self.snake = None

        self.algo = None
        self.snakes = []
        self.model_loaded = False

    
    def get_score(self):
        if self.snake:
            return self.snake.score
        else:
            return 0

    def get_steps(self):
        if self.snake:
            return self.snake.steps
        else:
            return 0

    def ate_fruit(self):
        if self.snake.ate_fruit():
            self.snake.add_body_ai()
            self.change_fruit_location()

    def change_fruit_location(self):
        while True:
            self.snake.create_fruit()
            position = self.snake.get_fruit()
            inside_body = False
            for body in self.snake.body:
                if position == body:
                    inside_body = True

            if inside_body == False:
                break


    def died(self):
        current_x = self.snake.body[0].x
        current_y = self.snake.body[0].y

        if not 0 <= current_x < NO_OF_CELLS:
            self.end = True
        elif not BANNER_HEIGHT <= current_y < NO_OF_CELLS:
            self.end = True
        elif self.snake.ate_body():
            self.end = True

    def get_fruit_pos(self):
        return self.snake.get_fruit()

    def set_algorithm(self, algo_type):
        if self.algo != None:
            return

        if algo_type == 'BFS':
            self.algo = BFS(self.grid)
            self.snake = Snake()

        elif algo_type == 'DFS':
            self.algo = DFS(self.grid)
            self.snake = Snake()

        elif algo_type == 'ASTAR':
            self.algo = A_STAR(self.grid)
            self.snake = Snake()


        elif algo_type == 'Greedy':
            self.algo = Greedy(self.grid)
            self.snake = Snake()

        elif algo_type == 'UCS':
            self.algo = UCS(self.grid)
            self.snake = Snake()

        elif algo_type == 'BestFS':
            self.algo = BestFirstSearch(self.grid)
            self.snake = Snake()

        

    def ai_play(self, algorithm):
        self.set_algorithm(algorithm)

        if self.algo == None:
            return

        pos = self.algo.run_algorithm(self.snake)
        self.update_path_finding_algo(pos)

    def keep_moving(self):
        x = self.snake.body[0].x
        y = self.snake.body[0].y

        if self.snake.body[1].x == x:
            if self.snake.body[1].y < y:
                # keep going down
                y = y + 1
            else:
                # keep going up
                y = y - 1
        elif self.snake.body[1].y == y:
            if self.snake.body[1].x < x:
                # keep going right
                x = x + 1
            else:
                # keep going left
                x = x - 1
        return x, y

    def update_GA_ai(self):
        if not self.snake and not self.model_loaded:
            if self.algo.done():
                if self.algo.next_generation():
                    self.snakes = self.algo.population.snakes
                else:
                    self.end = True

            for snake in self.snakes:
                x, y = self.algo.run_algorithm(snake)

                snake.move_ai(x, y)
                self.algo.died(snake)
                self.ate_fruit_GA(snake)
        else:
            x, y = self.algo.run_algorithm(self.snake)
            self.snake.move_ai(x, y)
            self.died()
            self.ate_fruit()

    def update_path_finding_algo(self, pos):
        if pos == None:
            x, y = self.keep_moving()
        else:
            x = pos.x
            y = pos.y

        self.snake.move_ai(x, y)
        self.died()
        self.ate_fruit()

        all_fruit_positions = self.get_all_fruit_positions()
        print("Fruit Positions:", all_fruit_positions)

    def get_all_fruit_positions(self):
        if self.snake:
            return [self.snake.get_fruit()]
