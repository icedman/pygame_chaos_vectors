from entities import entityService, Entity, EntityType, randomCorner
from state import gameState
from grid import grid
from maths import *
from enum import Enum
from grid import grid
from sounds import soundService, Effects


class PowerType(Enum):
    scoreUp = 0
    speedUp = 1
    shield = 2
    lifeUp = 3
    rearCannons = 4
    moreShots = 5
    shotSpeedUp = 6
    multiplier = 7
    bomb = 8
    superShots = 9
    none = 10


class PowerUp(Entity):
    defs = [
        PowerType.scoreUp,
        PowerType.speedUp,
        PowerType.speedUp,
        PowerType.speedUp,
        PowerType.speedUp,
        PowerType.shield,
        PowerType.shield,
        PowerType.shield,
        PowerType.lifeUp,
        PowerType.rearCannons,
        PowerType.rearCannons,
        PowerType.rearCannons,
        PowerType.moreShots,
        PowerType.moreShots,
        PowerType.moreShots,
        PowerType.moreShots,
        PowerType.shotSpeedUp,
        PowerType.shotSpeedUp,
        PowerType.multiplier,
        PowerType.bomb,
        # PowerType.superShots,
        PowerType.none,
    ]

    def init(self):
        Entity.init(self)
        self.radius = 20
        self.color = "white"
        self.polygon = 8
        self.speed = 2.5
        self.shield = 0
        self.max_count = 8
        self.life = 20000
        self.spawn_effect = Effects.spawn5

    def create(self):
        return PowerUp()

    def update(self, dt):
        px = gameState.player.pos.x
        py = gameState.player.pos.y

        dist = distance(px, py, self.pos.x, self.pos.y)
        if dist < self.radius + gameState.player.radius:
            self.activate()

    def blackhole(self):
        return

    def activate(self):
        e = self
        grid.push(e.pos.x, e.pos.y, 8, 1)
        entityService.destroy(e)
        entityService.attach(
            entityService.create(e.pos.x, e.pos.y, EntityType.explosion)
        )
        soundService.play(Effects.powerup)

        type = PowerType(self.defs[Rand(0, len(self.defs) - 1)])
        text = ""

        if not type in gameState.powers:
            gameState.powers[type] = 1
        else:
            gameState.powers[type] += 1

        for t in range(0, 4):
            max = 0
            if type == PowerType.speedUp:
                text = "speed"
                max = 4
            elif type == PowerType.shield:
                text = "shield"
                gameState.shield += 1
                if gameState.shield > 5:
                    gameState.shield = 5
            elif type == PowerType.rearCannons:
                text = "rear cannons"
            elif type == PowerType.moreShots:
                text = "triple shot"
            elif type == PowerType.shotSpeedUp:
                text = "shot speed"
                max = 4
            elif type == PowerType.multiplier:
                text = "multiplier"
                max = 4
            elif type == PowerType.bomb:
                text = "bomb"
                gameState.bombs += 1
                if gameState.bombs > 5:
                    gameState.bombs = 5
                break
            elif type == PowerType.lifeUp:
                text = "ship"
                gameState.ships += 1
                if gameState.ships > 5:
                    gameState.ships = 5
                break
            # elif type == PowerType.superShots:
            #     text = "super shots"
            else:
                points = 1000 * gameState.multipler
                gameState.score += points
                text = "+{}".format(points)
                break

            if max > 0 and gameState.powers[type] == max:
                continue
            break

        gameState.powers[type] = (
            max if gameState.powers[type] > max and max > 0 else gameState.powers[type]
        )

        entityService.createFloatingText(e.pos.x, e.pos.y, text, "red")


def updatePowers(dt):
    if gameState.gameOver:
        return

    gameState.power_gt += 1
    entities = entityService.entities

    gameState.multipler = 1
    if PowerType.multiplier in gameState.powers:
        gameState.multipler += gameState.powers[PowerType.multiplier]

    spawnEvery = 600
    if len(entities[EntityType.powerUp]) == 0:
        spawnEvery = 300

    if gameState.power_gt > spawnEvery and Rand(0, 100) < 20:
        corner = randomCorner(Rand(0, 12))
        gameState.power_gt = 0
        powerup = entityService.attach(
            entityService.create(corner.x, corner.y, EntityType.powerUp)
        )
        if powerup != None:
            soundService.play(powerup.spawn_effect)

    gameState.speed_player = 1.8
    if PowerType.speedUp in gameState.powers:
        gameState.speed_player += gameState.powers[PowerType.speedUp] * 0.5

    gameState.speed_shot = 6
    gameState.fire_rate = 150
    if PowerType.shotSpeedUp in gameState.powers:
        gameState.speed_shot += gameState.powers[PowerType.shotSpeedUp]
        gameState.fire_rate -= gameState.powers[PowerType.shotSpeedUp] * 25
    return
