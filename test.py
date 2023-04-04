from game import Game
from entities import EntityService
from grid import *

size = [800, 600]

game = Game()
game.setup(size)

game.update(0)

grid = Grid()
grid.init(800, 600)
grid.update(0)
