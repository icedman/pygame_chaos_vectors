from maths import *
from state import gameState
from entities import entityService, EntityType, randomCorner
from grid import grid
from particles import Particle, createParticles, createFloatingText
from player import Player
from powerup import PowerUp, updatePowers
from blackhole import RedCircle, pullParticles
from sounds import soundService, Effects


class Game:
    size = []

    def __init__(self):
        entityService.defs[EntityType.player] = Player()
        entityService.defs[EntityType.redCircle] = RedCircle()
        entityService.defs[EntityType.particle] = Particle()
        entityService.defs[EntityType.powerUp] = PowerUp()
        entityService.createParticles = createParticles
        entityService.createFloatingText = createFloatingText

    def setup(self, size):
        self.size = size
        gameState.screenWidth = size[0]
        gameState.screenHeight = size[1]
        self.newGame()

    def newGame(self, retainState=False):
        grid.init(self.size[0], self.size[1])
        if retainState != True:
            gameState.init()
        entityService.init()
        gameState.player = entityService.create(0, 0, EntityType.player)
        entityService.attach(gameState.player)

        # entityService.attach(entityService.create(100, 100, EntityType.pinkPinwheel))
        # entityService.attach(entityService.create(100, 100, EntityType.greenSquare))
        # entityService.attach(entityService.create(100, 100, EntityType.blueCircle))
        # entityService.attach(entityService.create(100, 100, EntityType.blueDiamond))
        # entityService.attach(entityService.create(100, 100, EntityType.purpleSquare))
        # entityService.attach(entityService.create(100, 100, EntityType.snake))
        # entityService.attach(entityService.create(100, 100, EntityType.redCircle))
        # entityService.attach(entityService.create(100, 100, EntityType.powerUp))
        # entityService.attach(entityService.create(100, 100, EntityType.redClone))
        # entityService.attach(entityService.create(100, 100, EntityType.generator))
        # for i in range(0, 10):
        #     entityService.attach(
        #         entityService.create(Rand(100, 800), Rand(100, 600), EntityType.lineEnd)
        #     )

        self.centerPlayer()

    def clear(self):
        entityService.init()

    def resetGame(self):
        if gameState.ships > 0:
            gameState.ships -= 1
            gameState.powers = {}
            gameState.shield = 1
            self.newGame(True)
        else:
            gameState.gameOver = True
            entityService.entities[EntityType.powerUp] = []

    def centerPlayer(self):
        gameState.player.pos.x = gameState.screenWidth / 2
        gameState.player.pos.y = gameState.screenHeight / 2

    def update(self, dt):
        gameState.tick += dt
        grid.update(dt)
        updatePowers(dt)

        entities = entityService.entities

        for k in entities.keys():
            ek = entities[k]
            for e in ek:
                entityService.update(e, dt)

        self.spawn(gameState.tick)

        pullParticles(gameState.tick)

        if gameState.dead_gt > 0:
            gameState.dead_gt -= 1
            if gameState.dead_gt <= 0:
                self.resetGame()

    def randomEnemy(self, gt, plus=0):
        sel = Min(Floor(gt / 1100), 8)
        rr = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9]]
        return EntityType(Rand(rr[sel][0], rr[sel][1]) + plus)

    def spawnEnemy(self, type, freeze, corner, gen=EntityType.none):
        corner = randomCorner(corner)
        x = corner.x
        y = corner.y

        # safe from player
        # player = gameState.player
        # pos = Vector(x, y)
        # ppos = Vector.copy(player.pos)
        # dist = pos.distanceTo(ppos)
        # if dist < player.radius * 2:
        #     print('move to safety')

        enemy = entityService.create(x, y, EntityType(type), freeze)

        enemy.generate_what = gen
        entityService.attach(enemy)

        soundService.play(enemy.spawn_effect)
        return enemy

    def spawn(self, t):
        # no spawn when..
        if gameState.gameOver:
            return
        if gameState.tick < 500:
            return
        if len(entityService.entities[EntityType.explosion]) > 0:
            return

        gtt = Floor(t / 20)
        if gtt == gameState.last_gt or gtt == 0:
            return

        gameState.last_gt = gtt
        gameState.spawn_gt += 1
        gt = gameState.spawn_gt

        # just random
        if ((gt / 350) % 2 < 1) and (gt % 33 < 1):
            self.spawnEnemy(self.randomEnemy(gt), 20, Rand(0, 12))

        # generator
        if gt % 444 < 1:
            gk = self.randomEnemy(gt / 3 + 500, 1)
            sz = Min(Rand(0, 16 + gt / 2000), 32)
            rate = Min(80 + Rand(0, 60) - gt / 1000, 60)
            if gk == EntityType.redClone:  # 'no clone generator
                gk = EntityType.butterfly  # 'butterfly generator
            while gk == EntityType.redCircle:  # 'no sun generator
                gk = EntityType(Rand(3, 5))  # 'green, purp, or blue;
            generator = self.spawnEnemy(EntityType.generator, 20, Rand(0, 12))
            generator.generate_rate = rate
            generator.generate_size = sz
            generator.generate_what = gk

        # some time base spawn computation
        gt4k = (gt % 4000) % 2 == 1 and (gt % 3333) == 0
        sp = [
            [(gt % 777 == 0), 0, 12, 3, 15, 24, 750, 2, 100, 5, 2 * 8, 24, 2, 1],
            [(gt % 1850 == 0), 0, 12, 2, 15, 24, 750, 2, 175, 5, 2 * 8, 24, 2, 1],
            [(gt % 2900 == 0), 5, 0, 2, 20, 40, 750, 3, 300, 5, 3 * 8, 24, 3, 1],
            [gt4k, 0, 11, 2, 20, 40, 750, 3, 300, 5, 3 * 8, 24, 3],
        ]

        if gameState.speed_enemy < 2 and gt % 888 == 0:
            gameState.speed_enemy += 0.1

        idx = 0
        for ss in sp:
            c = 0  # corner
            x = 0  # enemy type
            t = 0
            if ss[0]:
                c = Rand(ss[1], ss[2])
                x = self.randomEnemy(gt / ss[3])
                t = Min(Rand(ss[4], ss[5] + (gt / ss[6])) * ss[7], ss[8])
                if x == ss[9]:
                    t = ss[10]
                gameState.spawn_count[idx] = t
            idx += 1

        for idx in range(0, len(gameState.spawn_count)):
            ss = sp[idx]
            t = gameState.spawn_count[idx]
            if t > 0:
                t -= 1
                gameState.spawn_count[idx] = t
                if t % ss[12] == 0:
                    self.spawnEnemy(x, ss[11], c)
                    if x == EntityType.butterfly:  # ' 2X more indigo triangles'
                        self.spawnEnemy(x, ss[11], c)

        if gt % 50 * 60 == 1:  # 'every minute?
            inc = 0.15 + gameState.starting_difficulty * 0.1
            gameState.speed_nme += inc
