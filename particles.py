from entities import entityService, Entity, EntityType
from state import gameState
from maths import *


class Particle(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 2
        self.life = 1000
        self.speed = gameState.speed_particle
        self.max_count = 120
        self.direction = Vector.identity()

    def create(self):
        return Particle()

    def repel(self):
        return

    def kill(self):
        return


def initParticle(p, type=0, rot=0, sz=1):
    dir = 0
    mag = 0

    if type == 1:
        mag = 16
        p.direction.x = Cos(rot) * mag
        p.direction.y = Sin(rot) * mag
        p.active = 24

    elif type == 2:
        dir = rot
        mag = 8
        p.direction.x = Cos(dir) * mag
        p.direction.y = Sin(dir) * mag

    elif type == 8:
        #  3 dirs
        dir = 120 * Rand(0, 2) + rot
        mag = Rnd(3, 10)
        p.direction.x = Cos(dir) * mag
        p.direction.y = Sin(dir) * mag

    elif type == 3:
        #  4 dirs
        dir = 90 * Rand(0, 3) + rot
        mag = Rnd(3, 10)
        p.direction.x = Cos(dir) * mag
        p.direction.y = Sin(dir) * mag

    elif type == 6:
        #  8 dirs
        dir = 45 * Rand(0, 7) + rot
        mag = Rnd(3, 10)
        p.direction.x = Cos(dir) * mag
        p.direction.y = Sin(dir) * mag

    elif type == 7:
        #  any dir and speed
        mag = Rnd(0.5, 1)
        p.direction.x = Cos(rot) * mag
        p.direction.y = Sin(rot) * mag

    elif type == 9:
        #  bomb internal particles
        dir = Rand(0, 359)
        mag = Rnd(1, 13)
        p.direction.x = Cos(dir) * mag
        p.direction.y = Sin(dir) * mag

    else:
        #  random
        dir = Rand(0, 359)
        mag = Rnd(3, 10)
        p.direction.x = Cos(dir) * mag
        p.direction.y = Sin(dir) * mag

    p.direction.x = p.direction.x * 2
    p.direction.y = p.direction.y * 2
    p.pos.x += p.direction.x * sz
    p.pos.y += p.direction.y * sz


def createParticles(x, y, count, color, type=0, rot=0, sz=1):
    res = []
    for i in range(0, count):
        p = entityService.create(x, y, EntityType.particle)
        p.color = color
        initParticle(p, type, rot, sz)
        entityService.attach(p)
        res.append(p)
    return res


def createFloatingText(x, y, text, color):
    p = entityService.create(x, y, EntityType.floatingText)
    p.text = text
    p.color = color
    p.direction = Vector(0, -1)
    entityService.attach(p)
