import pygame
from Constants import *
from Menu import *
from GameController import GameController
import sys
import tkinter as tk

class GameGUI:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.SCREEN_UPDATE = pygame.USEREVENT

        self.speed = 10
        self.speed_up = 100

        pygame.time.set_timer(self.SCREEN_UPDATE, self.speed)

        self.controller = GameController()

        self.running, self.playing = True, False
        self.UPKEY, self.DOWNKEY, self.START, self.BACK = False, False, False, False

        self.SIZE = CELL_SIZE * NO_OF_CELLS
        self.display = pygame.Surface((self.SIZE, self.SIZE))
        self.window = pygame.display.set_mode((self.SIZE, self.SIZE))

        self.font_name = 'SquareAntiqua-Bold.ttf'

        self.main_menu = MainMenu(self)
        self.GA = GAMenu(self, self.controller)
        self.curr_menu = self.main_menu

        self.load_model = False
        self.view_path = False
        self.view_explored = False

    def game_loop(self):
        while self.playing:
            self.event_handler()

            if self.BACK:
                self.playing = False

            self.display.fill(WINDOW_COLOR)
            if self.controller.algo != None:
                self.draw_elements()
            self.window.blit(self.display, (0, 0))

            pygame.display.update()
            self.clock.tick(60)
            self.reset_keys()

    def draw_elements(self):
        # draw banner and stats
        self.draw_grid()
        self.draw_banner()
        self.draw_game_stats()
        self.draw_banner_text()
        self.draw_obstacles()  # Draw obstacles

        if self.curr_menu.state != 'GA' or self.controller.model_loaded:  # Path Ai or trained GA
            fruit = self.controller.get_fruit_pos()
            snake = self.controller.snake

            self.draw_fruit(fruit)
            self.draw_snake(snake)
            self.draw_score()
            self.draw_steps()

            if not self.controller.model_loaded:
                self.draw_path()  # only path Ai has a path

            self.draw_explored()

        else:  # training a GA model
            self.draw_all_snakes_GA()



    
    def draw_game_stats(self):
        if self.curr_menu.state != '':  # path Ai algo
            instruction = 'Space to view Ai path, W to stop, S to simulate,  Q to go back'

        # instruction
        self.draw_text(
            instruction, size=23,
            x=self.SIZE/2, y=(CELL_SIZE * NO_OF_CELLS) - NO_OF_CELLS*2,
            color= BLUE
        )

        # current Algo Title
        self.draw_text(
            self.curr_menu.state, size=40,
            x=self.SIZE/(2.5), y=CELL_SIZE +20,
        )

    def draw_path(self):
        if self.controller.algo != None and self.view_path:
            for path in self.controller.algo.path:  # for each {x,y} in path
                x = int(path.x * CELL_SIZE)
                y = int(path.y * CELL_SIZE)

                path_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

                shape_surf = pygame.Surface(path_rect.size, pygame.SRCALPHA)
                pygame.draw.rect(shape_surf, PATHCOLOR, shape_surf.get_rect())

                pygame.draw.rect(self.display, BANNER_COLOR, path_rect, 1)
                self.display.blit(shape_surf, path_rect)


    # Add this method to your GameGUI class
    def draw_explored(self):
        radius = 4
        if self.view_explored and self.controller.algo is not None :
            for node in self.controller.algo.explored_set:
                # Check if the node is inside the snake's body
                if not self.controller.algo.inside_body(self.controller.snake, node) :
                    self.draw_circle(node, color=EXPLORED_COLOR, radius=radius, border=True)

                
    def draw_snake_head(self, snake):
        head = snake.body[0]
        radius=20
        self.draw_circle(head, color=SNAKE_HEAD_COLOR, radius=radius, border=True)

    def draw_snake_body(self, body):
        radius = 20
        self.draw_circle(body, color=SNAKE_COLOR, radius=radius, border=True)


    def draw_rect(self, element, color, border=False):
        x = int(element.x * CELL_SIZE)
        y = int(element.y * CELL_SIZE)

        body_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.display, color, body_rect)

        if border:
            pygame.draw.rect(self.display, WINDOW_COLOR, body_rect, 3)

    def draw_circle(self, element, color, radius, border=False):
        x = int(element.x * CELL_SIZE) + CELL_SIZE // 2
        y = int(element.y * CELL_SIZE) + CELL_SIZE // 2

        pygame.draw.circle(self.display, color, (x, y), radius)

        if border:
            pygame.draw.circle(self.display, WINDOW_COLOR, (x, y), radius, 1)


    def draw_snake(self, snake):
        self.draw_snake_head(snake)  # draw head

        for body in snake.body[1:]:
            self.draw_snake_body(body)  # draw body

    

    def draw_fruit(self, fruit):
        x = int(fruit.x * CELL_SIZE)
        y = int(fruit.y * CELL_SIZE)

        fruit_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.display, FRUIT_COLOR, fruit_rect)

    def draw_banner(self):
        banner = pygame.Rect(0, 0, self.SIZE, BANNER_HEIGHT * CELL_SIZE)
        pygame.draw.rect(self.display, BANNER_COLOR, banner)

    def draw_score(self):
        score_text = 'Scores: ' + str(self.controller.get_score())
        score_x = self.SIZE - 700
        score_y = CELL_SIZE  # Adjust the y-coordinate to separate from the score
        self.draw_text(score_text, 20, score_x, score_y, WINDOW_COLOR)

    def draw_steps(self):
        steps_text = 'Steps: ' + str(self.controller.get_steps())
        steps_x = self.SIZE - 700
        steps_y = CELL_SIZE +30 # Adjust the y-coordinate to separate from the score
        self.draw_text(steps_text, 20, steps_x, steps_y, WINDOW_COLOR)


    def draw_banner_text(self):        
        steps_text = ' Nguyen Thanh Tinh\nHoang Huu Minh Phuc \nDinh Huu Quang Anh'
        
        steps_x = self.SIZE -150
        steps_y = CELL_SIZE + 20  # Adjust the y-coordinate to separate from the score
        self.draw_text(steps_text, 20, steps_x, steps_y, WINDOW_COLOR)


    def game_over(self):
        again = False

        while not again:
            for event in pygame.event.get():
                if self.is_quit(event):
                    again = True
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        again = True
                        break
                    if event.key == pygame.K_s:
                        again = True
                        self.controller.save_model()
                        break

            self.display.fill(MENU_COLOR)

            # training model results
            if  self.controller.model_loaded == False:

                # Path ai or trained model results
                high_score = f'High Score: {self.controller.get_score()}'
                step_score = f'Step : {self.controller.get_steps()}'

            to_continue = 'Enter to Continue'

            self.draw_text(
                high_score, size=35,
                x=self.SIZE/2, y=self.SIZE/2,
            )
            self.draw_text(
                step_score, size=35,
                x=self.SIZE/2, y=self.SIZE/2+20,
            )


            self.draw_text(
                to_continue, size=30,
                x=self.SIZE/2, y=self.SIZE/2 + 2*CELL_SIZE,
                color=WHITE
            )

            self.window.blit(self.display, (0, 0))
            pygame.display.update()
        self.controller.reset()

    def is_quit(self, event):
        # user presses exit icon
        if event.type == pygame.QUIT:
            self.running, self.playing = False, False
            self.curr_menu.run_display = False
            return True
        return False

    def event_handler(self):
        for event in pygame.event.get():
            if self.is_quit(event):
                pygame.quit()
                sys.exit()

            # user event that runs every self.speed milisec
            elif self.playing and event.type == pygame.USEREVENT:

                if self.load_model:  # user load model
                    self.controller.load_model()
                    self.load_model = False

                self.controller.ai_play(self.curr_menu.state)  # play

                if self.controller.end == True:  # Only path ai and trained model
                    self.playing = False
                    self.game_over()  # show game over stats

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:  # on Enter
                    self.START = True
                    self.view_path = False

                elif event.key == pygame.K_q:  # on q return
                    self.BACK = True
                    self.controller.reset()

                elif event.key == pygame.K_SPACE:  # space view path or hide training snakes
                    self.view_path = not self.view_path
                elif event.key == pygame.K_s:  # space view path or hide training snakes
                    self.view_explored = not self.view_explored
                elif event.key == pygame.K_DOWN:
                    self.DOWNKEY = True
                elif event.key == pygame.K_UP:
                    self.UPKEY = True

                elif event.key == pygame.K_w:  # speed up/down by self.speed_up
                    self.speed_up = -1 * self.speed_up
                    self.speed = self.speed + self.speed_up
                    pygame.time.set_timer(self.SCREEN_UPDATE, self.speed)

                # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #     x, y = pygame.mouse.get_pos()
                #     i, j = x // CELL_SIZE, y // CELL_SIZE

                #     # Toggle obstacle status when clicking on a cell
                #     cell = self.controller.grid[i][j]
                #     cell.is_obstacle = not cell.is_obstacle

    def reset_keys(self):
        self.UPKEY, self.DOWNKEY, self.START, self.BACK = False, False, False, False

    def draw_text(self, text, size, x, y, color=WINDOW_COLOR):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    # Add a new method to draw obstacles
    def draw_obstacles(self):
        for i in range(NO_OF_CELLS):
            for j in range(NO_OF_CELLS):
                current_node = self.controller.grid[i][j]

                if current_node.is_obstacle:
                    x = int(current_node.x * CELL_SIZE)
                    y = int(current_node.y * CELL_SIZE)
                    obstacle_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.display, OBSTACLE_COLOR, obstacle_rect)
                    pygame.draw.rect(self.display, WINDOW_COLOR, obstacle_rect, 1)

    # Modify the draw_grid method
    def draw_grid(self):
        color1 = (170, 203, 115)  
        color2 = (205, 233, 144)  # Lime green

        for i in range(NO_OF_CELLS):
            for j in range(NO_OF_CELLS):
                current_color = color1 if (i + j) % 2 == 0 else color2
                current_node = self.controller.grid[i][j]

                if current_node.is_obstacle:
                    pygame.draw.rect(self.display, OBSTACLE_COLOR, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(self.display, current_color, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.display, WINDOW_COLOR, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)