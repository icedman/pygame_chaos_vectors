from state import gameState
from maths import *
from enum import Enum
from particles import initParticle


class EntityType(Enum):
    pinkPinwheel = 0  # nme1 pinkPinwheel ~ 2.25
    blueDiamond = 1  # nme2 blueDiamonds ~ 3.25
    greenSquare = 2  # nme  greenSquare ~ 3.1
    purpleSquare = 3  # nme3 purpleSquares ~ 3.0
    blueCircle = 4  # nme4 blueCircles ~ 4.35
    redCircle = 5  # nme5 redCircles/blackhole ~ 2.5
    lineEnd = 6  # le   lineEnd ~ 2.0
    snake = 7  # nme6 snake ~ 3.5
    redClone = 8  # nme7 redClone 4.45
    butterfly = 9  # nme8 butterFlies ~ 5.0
    generator = 10  # ge   generator ~ 2.0
    snakeBody = 11
    player = 12
    shot = 13
    enemyShot = 14
    particle = 15


class Entity:
    type: EntityType = EntityType.pinkPinwheel
    pos: Vector = Vector()
    direction: Vector = Vector()

    max_count = -1
    speed = 1.0
    radius = 12
    color = "red"
    life = 0
    tick = 0
    freeze = 0
    toward_range = 0
    dodge = False
    wall = False
    text = ""

    def init(self):
        n = self
        dir = Rand(0, 359)
        mag = Rnd(2, 4)
        n.direction.x = Cos(dir) * mag
        n.direction.y = Sin(dir) * mag
        n.speed = self.speed * gameState.speed_nme

    def update(self, dt):
        # print('update')
        return

    def create(self):
        return Entity()

    def kill(self):
        e = self
        createFloatingText(e.pos.x, e.pos.y, "+20", e.color)
        createParticles(e.pos.x, e.pos.y, 4, e.color)
        entityService.destroy(e)

    def control(self):
        return

    def damp(self):
        e = self
        _speed = Sqr(e.direction.x * e.direction.x + e.direction.y * e.direction.y)
        if _speed > e.speed:
            e.direction.x = e.direction.x / _speed * e.speed
            e.direction.y = e.direction.y / _speed * e.speed

    def bound(self):
        e = self
        e.wall = False

        x = e.pos.x
        y = e.pos.y
        dx = e.direction.x
        dy = e.direction.y

        if x < 12:
            dx = Abs(dx)
            x = x + dx
            e.wall = True
        elif x > gameState.screen["width"] - 12:
            dx = -Abs(dx)
            x = x + dx
            e.wall = True

        if y < 12:
            dy = Abs(dy)
            y = y + dy
            e.wall = True
        elif y > gameState.screen["height"] - 12:
            dy = -Abs(dy)
            y = y + dy
            e.wall = True

        e.pos = Vector(x, y)
        e.direction = Vector(dx, dy)

    def toward(self, xx, yy, range):
        e = self
        ddx = xx - e.pos.x
        ddy = yy - e.pos.y
        dist = distance(xx, yy, e.pos.x, e.pos.y) + 0.001
        if dist < range:
            e.direction.x = e.direction.x + ddx / dist
            e.direction.y = e.direction.y + ddy / dist

    def repel(self):
        e = self
        for f in entityService.entities[e.type]:
            if f == e:
                continue
            distx = f.pos.x - e.pos.x
            disty = f.pos.y - e.pos.y
            dist = distance(f.pos.x, f.pos.y, e.pos.x, e.pos.y)
            if dist < e.radius * 1.8:
                e.direction.x -= Sgn(distx)
                e.direction.y -= Sgn(disty)

    def away(self, x1, y1, x2, y2):
        e = self
        x = e.pos.x
        y = e.pos.y
        dx = e.direction.x
        dy = e.direction.y

        ddx = x1 - x - (x1 - x2) * 4
        ddy = y1 - y - (y1 - y2) * 4
        bdx = x1 - x2
        bdy = y1 - y2
        distd = Sqr(ddx * ddx + ddy * ddy) + 0.001
        distb = Sqr(bdx * bdx + bdy * bdy) + 0.001

        if distd < 100:
            ddx = -ddx / distd * 30
            ddy = -ddy / distd * 30
            ddx += bdx / distb * 30
            ddy += bdy / distb * 30
            dx = dx + ddx
            dy = dy + ddy
            speed = Sqr(dx * dx + dy * dy)
            ns = n.speed * 1.1
            if speed > ns:
                dx = dx / speed * ns
                dy = dy / speed * ns

        e.direction = Vector(dx, dy)


def createParticles(x, y, count, color, type=0, sz=1):
    for i in range(0, count):
        p = entityService.create(x, y, EntityType.particle)
        p.color = color
        initParticle(p, type, sz)
        entityService.attach(p)


def createFloatingText(x, y, text, color):
    p = entityService.create(x, y, EntityType.particle)
    p.text = text
    p.color = color
    p.life = 1500
    p.direction = Vector(0, 1)
    entityService.attach(p)


class GreenSquare(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 16
        self.color = "green"
        self.speed = 3.1
        self.dodge = True
        self.toward_range = gameState.screen["width"]

    def create(self):
        return GreenSquare()


class PinkPinwheel(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 16
        self.color = "pink"
        self.speed = 2.25

    def create(self):
        return PinkPinwheel()


class BlueDiamond(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 18
        self.color = "aqua"
        self.speed = 3.25
        self.toward_range = gameState.screen["width"]

    def create(self):
        return BlueDiamond()


class Shot(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 10
        self.color = "yellow"
        self.speed = gameState.speed_shot

    def create(self):
        return Shot()

    def bound(self):
        # if bouncy .. base.bound
        e = self
        x = e.pos.x
        y = e.pos.y
        if (
            (x < 12)
            or (x > gameState.screen["width"] - 12)
            or (y < 12)
            or (y > gameState.screen["height"] - 12)
        ):
            createParticles(x, y, Rand(1, 3), e.color)
            entityService.destroy(e)

    def repel(self):
        return

    def update(self, dt):
        enemies = entityService.enemies

        e = self
        for k in enemies:
            for n in enemies[k]:
                dist = distance(n.pos.x, n.pos.y, e.pos.x, e.pos.y)
                if dist < (n.radius + e.radius):
                    entityService.destroy(e)
                    n.kill()
                    return


class Particle(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 4
        self.life = 1000
        self.speed = gameState.speed_particle


class Player(Entity):
    fx = 0
    fy = 0

    def init(self):
        Entity.init(self)
        self.radius = 12
        self.color = "white"
        dx = 0
        dy = 0

    def create(self):
        return Player()

    def control(self):
        speed_player = gameState.speed_player

        n = self
        keys = gameState.keys
        mx = -1 if (keys["a"] == True) else 0
        mx += 1 if (keys["d"] == True) else 0
        my = 1 if (keys["s"] == True) else 0
        my += -1 if (keys["w"] == True) else 0
        n.direction = Vector(
            mx * speed_player * gameState.speed_scale,
            my * speed_player * gameState.speed_scale
        )

        fx = 1 if (keys["right"] == True) else 0
        fx += -1 if (keys["left"] == True) else 0
        fy = 1 if (keys["down"] == True) else 0
        fy += -1 if (keys["up"] == True) else 0

        if (fx or fy) and (
            gameState.tick - entityService.last_shot
        ) > gameState.fire_rate:
            shot = entityService.create(n.pos.x, n.pos.y, EntityType.shot)
            shot.direction = Vector(
                fx * shot.speed,
                fy * shot.speed
            )
            entityService.last_shot = gameState.tick
            entityService.attach(shot)

    def update(self, dt):
        enemies = entityService.enemies

        e = self
        e.color = "white"
        for k in enemies:
            for n in enemies[k]:
                dist = distance(n.pos.x, n.pos.y, e.pos.x, e.pos.y)
                if dist < (n.radius + e.radius):
                    e.color = "red"
                    n.kill()
                    return


class EntityService:
    last_shot = 0
    entities: dict[EntityType, list] = {}
    enemies: dict[EntityType, list] = {}

    defs: dict[EntityType, Entity] = {
        EntityType.pinkPinwheel: PinkPinwheel(),
        EntityType.blueDiamond: BlueDiamond(),
        EntityType.greenSquare: GreenSquare(),
        EntityType.purpleSquare: Entity(),
        EntityType.blueCircle: Entity(),
        EntityType.redCircle: Entity(),
        EntityType.lineEnd: Entity(),
        EntityType.snake: Entity(),
        EntityType.redClone: Entity(),
        EntityType.butterfly: Entity(),
        EntityType.generator: Entity(),
        EntityType.snakeBody: Entity(),
        EntityType.player: Player(),
        EntityType.shot: Shot(),
        EntityType.enemyShot: Entity(),
        EntityType.particle: Particle(),
    }

    def init(self):
        for k in self.defs.keys():
            self.entities[k] = []
            self.enemies[k] = self.entities[k]

        # not enemies
        self.enemies[EntityType.player] = []
        self.enemies[EntityType.shot] = []
        self.enemies[EntityType.enemyShot] = []
        self.enemies[EntityType.particle] = []

    def create(self, x, y, what, freeze=0):
        e = self.defs[what].create()
        e.init()
        e.pos = Vector(x, y)
        e.type = what
        e.freeze = freeze * 100
        return e

    def attach(self, e):
        base = self.defs[e.type]
        if base.max_count > 0 and len(self.entities[e.type]) >= base.max_count:
            return
        self.entities[e.type].append(e)

    def destroy(self, e: Entity):
        idx = self.entities[e.type].index(e)
        if idx != -1:
            del self.entities[e.type][idx]

    def update(self, e: Entity, dt):
        e.tick += dt
        if e.life > 0 and e.tick > e.life:
            self.destroy(e)
            return

        if e.freeze > 0:
            e.freeze -= dt
            return

        e.control()

        x = e.pos.x
        y = e.pos.y
        dx = e.direction.x
        dy = e.direction.y

        x = x + dx * gameState.speed_scale
        y = y + dy * gameState.speed_scale
        e.pos = Vector(x, y)

        player = gameState.player
        e.bound()

        if not player is None and e.toward_range > 0:
            e.toward(player.pos.x, player.pos.y, e.toward_range)

        e.repel()
        e.update(dt)
        e.damp()


entityService = EntityService()
