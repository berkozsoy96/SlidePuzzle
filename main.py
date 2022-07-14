import pygame as pg
from enum import Enum
import numpy as np


def load_image(name, colorkey=None, scale=1):
    image = pg.image.load(name)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


Directions = {
    "UP": (0, 1),
    "DOWN": (0, -1),
    "LEFT": (1, 0),
    "RIGHT": (-1, 0)
}


class Square(pg.sprite.Sprite):
    def __init__(self, number, position: tuple):
        if number != -1:
            pg.sprite.Sprite.__init__(self)  # call Sprite initializer
            self.number = number
            self.image, self.rect = load_image("square.bmp", -1, 1)
            self.rect.topleft = (10 + position[0] * self.image.get_size()[0], 10 + position[1] * self.image.get_size()[1])

    def move(self, direction: Directions):
        self.rect = self.rect.move((direction[0] * self.image.get_size()[0], direction[1] * self.image.get_size()[1]))
        print(f"{self.number} moved {direction}")


class Game(pg.sprite.Sprite):
    def __init__(self, grid_size):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.grid_size = grid_size
        self.empty_grid_position = (self.grid_size-1, self.grid_size-1)
        self.grid = self.prep_grid()

    def prep_grid(self):
        grid = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                row.append(Square(i * self.grid_size + j, (i, j)))
            grid.append(row)
        grid = np.array(grid)
        grid[-1, -1] = Square(-1, self.empty_grid_position)
        return grid

    def move(self, direction: Directions):
        sq_pos = (self.empty_grid_position[0] - direction[0], self.empty_grid_position[1] - direction[1])
        if 0 <= sq_pos[0] < self.grid_size and 0 <= sq_pos[1] < self.grid_size:
            sq = self.grid[sq_pos[0], sq_pos[1]]
            sq.move(direction)
            self.grid[sq_pos[0], sq_pos[1]], self.grid[self.empty_grid_position[0], self.empty_grid_position[1]] = self.grid[self.empty_grid_position[0], self.empty_grid_position[1]], self.grid[sq_pos[0], sq_pos[1]]
            self.empty_grid_position = sq_pos


pg.init()
screen = pg.display.set_mode((700, 700), pg.SCALED)
pg.display.set_caption("SlidePuzzle")

background = pg.Surface(screen.get_size())
background = background.convert()
background.fill((61, 63, 65))
screen.blit(background, (0, 0))
pg.display.flip()

game = Game(4)
allsprites = pg.sprite.RenderPlain(game.grid.flatten()[:4**2-1])

going = True
while going:
    for event in pg.event.get():
        match event.type:
            case pg.QUIT:
                going = False
            case pg.KEYDOWN:
                match event.key:
                    case pg.K_ESCAPE:
                        going = False
                    case pg.K_UP:
                        game.move(Directions["UP"])
                    case pg.K_DOWN:
                        game.move(Directions["DOWN"])
                    case pg.K_LEFT:
                        game.move(Directions["LEFT"])
                    case pg.K_RIGHT:
                        game.move(Directions["RIGHT"])
    allsprites.update()
    screen.blit(background, (0, 0))
    allsprites.draw(screen)
    pg.display.flip()
pg.quit()
