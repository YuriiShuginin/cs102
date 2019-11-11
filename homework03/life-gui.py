import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI

class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j]:
                    col = pygame.Color('green')
                else:
                    col = pygame.Color('white')
                pygame.draw.rect(self.screen, col, (j * self.cell_size + 1, i * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        paused = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                        if event.key == K_RSHIFT:
                            paused = not paused

            self.draw_lines()
            self.draw_grid()
            pygame.display.flip()

            while paused:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                        paused = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            click_pos = pygame.mouse.get_pos()
                            x = click_pos[0] // self.cell_size
                            y = click_pos[1] // self.cell_size
                            self.life.curr_generation[y][x] = (self.life.curr_generation[y][x] + 1) % 2
                            self.draw_lines()
                            self.draw_grid()
                            pygame.display.flip()
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_RSHIFT:
                            paused = not paused

            self.life.step()
            if self.life.is_max_generations_exceeded or not self.life.is_changing:
                running = False
            clock.tick(self.speed)
        pygame.quit()


if __name__ == '__main__':
    game = GameOfLife((12, 16), max_generations = 50)
    gui = GUI(game)
    gui.run()