from entities import entityService, Entity, EntityType
from state import gameState
from grid import grid
from maths import *
from powerup import PowerType


class Player(Entity):
    last_direction = Vector(0, 1)

    mRotateLeft = Matrix.identity().rotate(0, 90, 180 * 3.14 / 180)
    mRotateRight = Matrix.identity().rotate(0, 270, 180 * 3.14 / 180)
    mRotate180 = Matrix.identity().rotate(0, 0, 180 * 3.14 / 180)
    mRotate30 = Matrix.identity().rotate(0, 0, 15 * 3.14 / 180)
    mRotate330 = Matrix.identity().rotate(0, 0, 345 * 3.14 / 180)

    space_gt = 0
    dead_gt = 0

    def init(self):
        Entity.init(self)
        self.radius = 16
        self.color = "white"
        self.shape = "ship"
        self.rotate_toward = True
        self.direction = Vector()
        self.space_gt = 0
        self.dead_gt = 0

    def create(self):
        return Player()

    def shoot(self, direction):
        shot = entityService.create(self.pos.x, self.pos.y, EntityType.shot)
        shot.direction = direction
        entityService.attach(shot)

    def control(self):
        if gameState.tick < 500:
            return

        speed_player = gameState.speed_player
        shotspeed = gameState.speed_shot

        n = self
        keys = gameState.keys
        mx = -1 if (keys["a"] == True) else 0
        mx += 1 if (keys["d"] == True) else 0
        my = 1 if (keys["s"] == True) else 0
        my += -1 if (keys["w"] == True) else 0
        ndir = Vector(
            mx * speed_player * gameState.speed_scale,
            my * speed_player * gameState.speed_scale,
        )

        if keys[" "] and gameState.bombs > 0:
            if len(entityService.entities[EntityType.bomb]) == 0:
                bomb = entityService.create(self.pos.x, self.pos.y, EntityType.bomb)
                entityService.attach(bomb)
                gameState.bombs -= 1

        n.direction.scale(2)
        ndir.scale(3)
        n.direction.add(ndir)
        n.direction.scale(0.5)

        if mx != 0 or my != 0:
            self.last_direction = Vector(mx, my)

        fx = 1 if (keys["right"] == True) else 0
        fx += -1 if (keys["left"] == True) else 0
        fy = 1 if (keys["down"] == True) else 0
        fy += -1 if (keys["up"] == True) else 0

        a = angleTo(0, 0, n.last_direction.x, n.last_direction.y) + 360
        n.angle += 360
        n.angle *= 4
        n.angle += a
        n.angle /= 5
        n.angle -= 360

        if (fx or fy) and (
            gameState.tick - entityService.last_shot
        ) > gameState.fire_rate:
            entityService.last_shot = gameState.tick

            shotdir = Vector(fx * shotspeed, fy * shotspeed)
            self.shoot(shotdir)

            if PowerType.rearCannons in gameState.powers:
                rearShot = Vector.copy(shotdir).transform(self.mRotate180)
                self.shoot(rearShot)

            if PowerType.moreShots in gameState.powers:
                shot2 = Vector.copy(shotdir).transform(self.mRotate30)
                self.shoot(shot2)
                shot3 = Vector.copy(shotdir).transform(self.mRotate330)
                self.shoot(shot3)

    def update(self, dt):
        enemies = entityService.enemies

        e = self

        # die from enemies
        e.color = "white"
        for k in enemies:
            for n in enemies[k]:
                if n.freeze > 0:
                    continue
                dist = distance(n.pos.x, n.pos.y, e.pos.x, e.pos.y)
                if dist < (n.radius + e.radius):
                    e.color = "red"
                    n.kill(self)
                    # print("{} {} - {} {}".format(n.pos.x, n.pos.y, self.pos.x, self.pos.y))
                    if gameState.shield > 0:
                        gameState.shield -= 0.25
                    else:
                        self.kill(n)
                        explosion = entityService.create(
                            self.pos.x, self.pos.y, EntityType.explosion
                        )
                        explosion.life *= 2
                        entityService.attach(explosion)
                    return

    def kill(self, killer):
        self.dead_gt = 100
        Entity.kill(self, killer)
