import pygame
from maths import *
from game import Game
from state import gameState
from draw import Context
from grid import grid
from entities import entityService
from renderer import Renderer, renderShape, renderGrid
from sounds import soundService, Effects
from powerup import PowerType

pygame.init()
size = [1600, 900]
# size = [1280, 800]
screen = pygame.display.set_mode(size)
done = False
gfx = Context(screen)

game = Game()
game.setup(size)

paused = False
menu_gt = 0
last_tick = 0


def enter_scene(scn):
    gameState.scene = scn
    if gameState.scene == 0:
        game.clear()
    elif gameState.scene == 1:
        game.newGame()


def game_loop(dt):
    if paused == False:
        game.update(dt)

    gfx.clear("black")

    gfx.save()
    gfx.drawRect(1, 1, size[0], size[1], "red")
    renderGrid(gfx)

    entities = entityService.entities
    for k in entities.keys():
        ek = entities[k]
        for e in ek:
            Renderer.renderEntity(gfx, e)

    gfx.restore()

    # draw heads-up
    gfx.drawText(size[0] - 10, 40, "{}".format(gameState.score), 1.5, "magenta", 2)
    gfx.drawText(15, 40, "Ships:{}".format(gameState.ships), 1.5, "magenta", 1)
    gfx.drawText(200, 40, "Bombs:{}".format(gameState.bombs), 1.5, "magenta", 1)
    gfx.drawText(400, 40, "x{}".format(gameState.multipler), 1.5, "magenta", 1)

    if gameState.gameOver:
        gfx.drawText(size[0] / 2, size[1] / 2, "Game Over", 2, "red")
        if pressed[pygame.K_SPACE]:
            enter_scene(0)

    pygame.display.flip()


def menu_loop(dt):
    gfx.clear("black")

    gfx.save()
    gfx.drawRect(1, 1, size[0], size[1], "red")
    renderGrid(gfx)

    if menu_gt % 60 == 0:
        if RndOr(0, 1) == 0:
            grid.push(Rand(0, size[0]), Rand(0, size[1]), 6, 1 + Rand(0, 2))
        else:
            grid.pull(Rand(0, size[0]), Rand(0, size[1]), 8, 6 + Rand(0, 4))

    grid.update(dt)

    gfx.saveAttributes()
    gfx.state.strokeWidth = 4
    gfx.drawText(size[0] / 2, size[1] / 2, "Chaos Vectors", 4, "yellow")
    gfx.restore()
    gfx.drawText(size[0] / 2, size[1] / 2 + 150, "Press SPACE to play", 1.5, "white")
    gfx.drawText(size[0] / 2, size[1] - 120 + 0, "W,A,S,D to move", 1, "gray")
    gfx.drawText(
        size[0] / 2, size[1] - 120 + 25, "Up, Down, Left, Right to shoot", 1, "gray"
    )
    gfx.drawText(size[0] / 2, size[1] - 120 + 50, "Space to explode bomb", 1, "gray")

    if menu_gt > 50 and pressed[pygame.K_SPACE]:
        enter_scene(1)

    entities = entityService.entities
    for k in entities.keys():
        ek = entities[k]
        for e in ek:
            entityService.update(e, dt)
            Renderer.renderEntity(gfx, e)

    pygame.display.flip()


# setup sounds
#
soundService.defs[Effects.spawn1] = pygame.mixer.Sound("./sounds/draven/spawn/d6.wav")
# generator
soundService.defs[Effects.spawn2] = pygame.mixer.Sound("./sounds/draven/spawn/d1.wav")
soundService.defs[Effects.spawn3] = pygame.mixer.Sound(
    "./sounds/sounds/buttonselect/1.wav"
)
soundService.defs[Effects.spawn4] = pygame.mixer.Sound(
    "./sounds/sounds/buttonselect/4.wav"
)
# powerup
soundService.defs[Effects.spawn5] = pygame.mixer.Sound(
    "./sounds/sounds/buttonselect/7.wav"
)

soundService.defs[Effects.shot] = pygame.mixer.Sound("./sounds/draven/spawn/d6.wav")
soundService.defs[Effects.destroy] = pygame.mixer.Sound("./sounds/draven/spawn/d3.wav")
soundService.defs[Effects.powerup] = pygame.mixer.Sound(
    "./sounds/jalastram/powerup.mp3"
)
soundService.defs[Effects.explosion] = pygame.mixer.Sound("./sounds/draven/bomb.wav")

for d in soundService.defs:
    soundService.defs[d].set_volume(0.25)

enter_scene(0)
while not done:
    tick = pygame.time.get_ticks()
    dt = tick - last_tick
    if dt < 24:
        continue
    last_tick = tick
    menu_gt += 1

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
    gameState.keys["p"] = pressed[pygame.K_p]

    released = []
    for k in gameState.last_pressed:
        if gameState.keys[k] == False:
            released.append(k)

    gameState.last_pressed = []
    for k in gameState.keys:
        if gameState.keys[k]:
            gameState.last_pressed.append(k)

    if "p" in released:
        paused = not paused

    if gameState.scene == 0:
        menu_loop(dt)
    elif gameState.scene == 1:
        game_loop(dt)
        menu_gt = 0

    for r in soundService.requests:
        cnt = soundService.requests[r]
        del soundService.requests[r]
        snd = soundService.defs[r]
        pygame.mixer.Sound.stop(snd)
        pygame.mixer.Sound.play(snd)
        break
