import pygame
from maths import *
from game import Game
from state import gameState
from draw import Context

pygame.init()
size = [800, 600]
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
    if dt < 48:
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

    gfx.save()
    
    gfx.save()
    gfx.rotate(rot * 3.14 / 180)
    gfx.scale(2, 2)
    gfx.translate(400, 200)
    gfx.drawPolygon(0, 0, 120, 5, 'red')
    gfx.restore()

    rot = (rot + 1) % 360

    entities = game.entities()
    for k in entities.keys():
        ek = entities[k]
        for e in ek:
            gfx.drawLine(
                e.pos.x - e.radius / 2,
                e.pos.y - e.radius / 2,
                e.pos.x + e.radius / 2,
                e.pos.y + e.radius / 2,
                e.color,
            )
            if e.text != '':
                gfx.drawText(e.pos.x, e.pos.y, e.text, 2, e.color)

    gfx.restore()
    pygame.display.flip()
