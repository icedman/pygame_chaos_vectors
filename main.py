import pygame
import sys

from maths import *
from game import Game
from state import gameState
from draw import Context
from grid import grid
from entities import entityService
from renderer import Renderer, renderGrid
from sounds import soundService, Effects
from powerup import PowerType
from colors import tint, untint
from scene import *
from demo import *

pygame.init()
# size = [1600, 900]
size = [1280, 800]
screen = pygame.display.set_mode(size)
gfx = Context(screen)

game = Game()
game.setup(size)

menu_gt = 0
last_tick = 0

# def enter_scene(scn):
#     gameState.scene = scn
#     if gameState.scene == 0:
#         game.clear()
#     elif gameState.scene == 1:
#         game.newGame()


def toggleTint():
    gameState.tinted = not gameState.tinted
    if gameState.tinted:
        tint(0, 255, 0, 0.6)
    else:
        untint()


def game_update(dt):
    if gameState.paused == False:
        game.update(dt)

    if gameState.released["escape"]:
        sceneService.enterScene(SceneType.menu)


def game_render(gfx):
    gfx.clear("black")

    gfx.save()
    gfx.drawRect(1, 1, size[0] - 2, size[1], "red")
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
        if gameState.released[" "]:
            sceneService.enterScene(SceneType.menu)


def menu_update(dt):
    if menu_gt % 60 == 0:
        if RndOr(0, 1) == 0:
            grid.push(Rand(0, size[0]), Rand(0, size[1]), 6, 1 + Rand(0, 2))
        else:
            grid.pull(Rand(0, size[0]), Rand(0, size[1]), 8, 6 + Rand(0, 4))
    grid.update(dt)


def menu_render(gfx):
    gfx.clear("black")
    gfx.save()
    gfx.drawRect(1, 1, size[0] - 2, size[1], "red")
    renderGrid(gfx)

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

    if gameState.released[" "]:
        sceneService.enterScene(SceneType.game)

    entities = entityService.entities
    for k in entities.keys():
        ek = entities[k]
        for e in ek:
            entityService.update(e, dt)
            Renderer.renderEntity(gfx, e)


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

gameState.trackedKeys = {
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
    pygame.K_ESCAPE: "escape",
    pygame.K_SPACE: " ",
    pygame.K_w: "w",
    pygame.K_a: "a",
    pygame.K_s: "s",
    pygame.K_d: "d",
    pygame.K_p: "p",  # pause
    pygame.K_t: "t",  # toggle sound
    pygame.K_o: "o",  # demo
    pygame.K_l: "l",  # basicDraw
}
gameState.init()
gameState.screenWidth = size[0]
gameState.screenHeight = size[1]


class GameScene:
    type = SceneType.menu

    def onEnter(self):
        game.newGame()
        pass

    def onExit(self):
        pass

    def onUpdate(self, dt):
        game_update(dt)

    def onRender(self, gfx):
        game_render(gfx)


class MenuScene:
    type = SceneType.menu

    def onEnter(self):
        game.clear()
        menu_gt = 0

    def onExit(self):
        pass

    def onUpdate(self, dt):
        menu_update(dt)

        if gameState.released["escape"]:
            gameState.done = True

    def onRender(self, gfx):
        menu_render(gfx)


sceneService.defs[SceneType.menu] = MenuScene()
sceneService.defs[SceneType.game] = GameScene()
sceneService.defs[SceneType.demo] = DemoScene()
sceneService.enterScene(SceneType.menu)

for arg in sys.argv:
    if arg.startswith("-"):
        gameState.pressed[arg[1:]] = True

while not gameState.done:
    released = []

    tick = pygame.time.get_ticks()
    dt = tick - last_tick
    if dt < 24:
        continue
    last_tick = tick
    menu_gt += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameState.done = True

    pressed = pygame.key.get_pressed()
    for k in gameState.trackedKeys:
        hk = gameState.trackedKeys[k]
        gameState.released[hk] = gameState.pressed[hk] == True and pressed[k] == False
        gameState.pressed[hk] = pressed[k]

    if gameState.released["p"]:
        gameState.paused = not gameState.paused
    if gameState.released["t"]:
        toggleTint()
    if gameState.released["o"]:
        sceneService.enterScene(SceneType.demo)
    if gameState.released["l"]:
        gfx.basicDraw = not gfx.basicDraw

    sceneService.current.onUpdate(dt)
    sceneService.current.onRender(gfx)
    pygame.display.flip()

    for r in soundService.requests:
        cnt = soundService.requests[r]
        del soundService.requests[r]
        snd = soundService.defs[r]
        pygame.mixer.Sound.stop(snd)
        pygame.mixer.Sound.play(snd)
        break
