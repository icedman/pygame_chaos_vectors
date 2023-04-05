import pygame
from maths import *
from game import Game
from state import gameState
from draw import Context
from entities import entityService
from renderer import Renderer, renderShape, renderGrid

pygame.init()
size = [1280, 800]
screen = pygame.display.set_mode(size)
done = False
gfx = Context(screen)

game = Game()
game.setup(size)

last_tick = 0
rot = 0

while not done:
    tick = pygame.time.get_ticks()
    dt = tick - last_tick
    if dt < 24:
        continue
    last_tick = tick

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()
    gameState.keys["w"] = pressed[pygame.K_w]
    gameState.keys["a"] = pressed[pygame.K_a]
    gameState.keys["s"] = pressed[pygame.K_s]
    gameState.keys["d"] = pressed[pygame.K_d]

    gameState.keys["left"] = pressed[pygame.K_LEFT]
    gameState.keys["right"] = pressed[pygame.K_RIGHT]
    gameState.keys["up"] = pressed[pygame.K_UP]
    gameState.keys["down"] = pressed[pygame.K_DOWN]

    game.update(dt)

    gfx.clear("black")
    gfx.drawRect(1, 1, size[0], size[1], "red")
    renderGrid(gfx)

    gfx.save()

    # gfx.save()
    # gfx.rotate(rot)
    # rot = (rot + 1) % 360
    # gfx.scale(2, 2)
    # gfx.translate(400, 200)
    # gfx.drawPolygon(0, 0, 120, 5, 'red')
    # gfx.restore()
    # renderShape(gfx, 'square_diamond', 200, 200, 40)

    entities = entityService.entities
    for k in entities.keys():
        ek = entities[k]
        for e in ek:
            Renderer.renderEntity(gfx, e)

    gfx.restore()

    # draw heads-up
    gfx.drawText(size[0] - 10, 40, "{}".format(gameState.score), 1.5, "yellow", 2)
    gfx.drawText(15, 40, "Ships:{}".format(gameState.ships), 1.5, "yellow", 1)
    pygame.display.flip()
