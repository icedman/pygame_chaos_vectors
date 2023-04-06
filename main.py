import pygame
from maths import *
from game import Game
from state import gameState
from draw import Context
from entities import entityService
from renderer import Renderer, renderShape, renderGrid

pygame.init()
# size = [1800, 900]
size = [1280, 800]
screen = pygame.display.set_mode(size)
done = False
gfx = Context(screen)

game = Game()
game.setup(size)

render_gt = 0
last_tick = 0

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
    if pressed[pygame.K_ESCAPE]:
        break

    gameState.keys["w"] = pressed[pygame.K_w]
    gameState.keys["a"] = pressed[pygame.K_a]
    gameState.keys["s"] = pressed[pygame.K_s]
    gameState.keys["d"] = pressed[pygame.K_d]
    gameState.keys[" "] = pressed[pygame.K_SPACE]

    gameState.keys["left"] = pressed[pygame.K_LEFT]
    gameState.keys["right"] = pressed[pygame.K_RIGHT]
    gameState.keys["up"] = pressed[pygame.K_UP]
    gameState.keys["down"] = pressed[pygame.K_DOWN]

    game.update(dt)

    # if render_gt < 2:
    #     render_gt += 1
    #     continue
    # render_gt = 0

    gfx.clear("black")

    gfx.save()
    gfx.drawRect(1, 1, size[0], size[1], "red")
    renderGrid(gfx)

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
    gfx.drawText(200, 40, "Bombs:{}".format(gameState.bombs), 1.5, "yellow", 1)
    gfx.drawText(400, 40, "x{}".format(gameState.multiplier()), 1.5, "yellow", 1)

    if gameState.gameOver:
        gfx.drawText(size[0] / 2, size[1] / 2, "Game Over", 2, "red")
        if pressed[pygame.K_SPACE]:
            game.newGame()

    pygame.display.flip()
