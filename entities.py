from state import gameState
from maths import *
from enum import Enum
from grid import grid
from sounds import soundService, Effects


def randomCorner(c):
    x = 0
    y = 0
    corner = Floor(c)

    if corner > 4 and corner < 12:
        pair = [
            [],
            [],
            [],
            [],
            [],
            [1, 4],
            [1, 2],
            [2, 3],
            [3, 4],
            [1, 3],
            [1, 4],
            [2, 4],
        ]
        p = pair[corner]
        corner = Rand(1, 4) if (corner == 5) else RndOr(p[0], p[1])

    if corner < 5:
        pw = gameState.screen["width"]
        ph = gameState.screen["height"]
        cp = [
            [30, pw - 30, 30, ph - 30],
            [30, 80, 30, 80],
            [pw - 80, pw - 30, 30, 80],
            [pw - 80, pw - 30, ph - 80, ph - 30],
            [30, 80, ph - 80, ph - 30],
        ][corner]
        x = Rand(cp[0], cp[1])
        y = Rand(cp[2], cp[3])
    else:
        angle = Rand(0, 360)
        mag = 240
        x = gameState.player.pos.x + Cos(angle) * mag
        y = gameState.player.pos.y + Sin(angle) * mag

    return Vector(x, y)


class EntityType(Enum):
    pinkPinwheel = 0
    blueDiamond = 1
    greenSquare = 2
    purpleSquare = 3
    blueCircle = 4
    redCircle = 5
    lineEnd = 6
    snake = 7
    redClone = 8
    butterfly = 9
    generator = 10
    snakeBody = 11
    player = 12
    shot = 13
    enemyShot = 14
    particle = 15
    floatingText = 16
    powerUp = 17
    bomb = 18
    explosion = 19
    none = 99


class Entity:
    type: EntityType = EntityType.none
    pos: Vector = Vector()
    direction: Vector = Vector()

    max_count = 30
    speed = 1.0
    radius = 12
    color = "red"
    points = 20
    shape = ""
    polygon = 0
    life = 0
    tick = 0
    freeze = 0
    toward_range = 0
    rotate_toward = False
    angle = 0
    spin_speed = 0
    dodge = False
    wall = False
    text = ""
    shield = 0

    # snake & line
    rotation = 0
    rotation_dir = 0
    headNode = None
    nextNode = None

    # generator
    generate_rate = 0
    generate_what: EntityType = EntityType.none
    generate_size = 0

    # hints
    angle_offset = 0
    spawn_effect = Effects.none

    def init(self):
        n = self
        dir = Rand(0, 359)
        mag = Rnd(2, 4)
        n.direction.x = Cos(dir) * mag
        n.direction.y = Sin(dir) * mag
        n.spin_speed = Rnd(1, 4)
        n.speed = self.speed * gameState.speed_enemy

    def update(self, dt):
        # print('update')
        return

    # todo add movements
    # zigzag (line & snake)
    # intercept
    # square
    # lines

    def create(self):
        return Entity()

    def kill(self, killer):
        e = self
        if e.points > 0:
            points = e.points * gameState.multipler
            entityService.createFloatingText(
                e.pos.x, e.pos.y, "+{}".format(points), e.color
            )
            gameState.score += points
        entityService.createParticles(e.pos.x, e.pos.y, 8, e.color)
        entityService.destroy(e)
        soundService.play(Effects.destroy)
        grid.push(e.pos.x, e.pos.y, 8, 1)

        return True

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

    def blackhole(self):
        blackhole_list = entityService.entities[EntityType.redCircle]
        for blackhole in blackhole_list:
            if blackhole.active:
                ddx = blackhole.pos.x - self.pos.x
                ddy = blackhole.pos.y - self.pos.y
                dist = Sqr(ddx * ddx + ddy * ddy) + 0.001
                dx = self.direction.x
                dy = self.direction.y
                if dist < 75 + blackhole.size * 8:
                    dx = dx + ddx / dist / 512 * (1200 - dist)
                    dy = dy + ddy / dist / 512 * (1200 - dist)
                    self.direction = Vector(dx, dy)

                    rr = self.radius + (blackhole.size / 10)
                    # if dist < 12 + blackhole.size / 2:
                    if dist < rr:
                        self.points = 0
                        if self.kill(blackhole):
                            blackhole.grow(1)
                        break


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
        self.points = 20
        self.shape = "pinwheel"
        self.spawn_effect = Effects.spawn3

    def create(self):
        return PinkPinwheel()


class BlueDiamond(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 18
        self.color = "cyan"
        self.speed = 3.25
        self.points = 50
        self.toward_range = gameState.screen["width"]
        self.spawn_effect = Effects.spawn3

    def create(self):
        return BlueDiamond()


class PurpleSquare(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 16
        self.color = "purple"
        self.speed = 3
        self.toward_range = gameState.screen["width"]
        self.max_count = 120
        self.points = 100
        self.shape = "square_diamond"
        self.spawn_effect = Effects.spawn3

    def create(self):
        return PurpleSquare()

    def kill(self, killer):
        e = self
        if e.radius != 16:
            Entity.kill(e, killer)
            return

        entityService.destroy(e)

        # spawn thingys
        ro = RndOr(2, 3)
        for i in range(0, ro):
            c = entityService.create(
                e.pos.x + Rand(-30, 30), e.pos.y + Rand(-30, 30), e.type
            )
            c.radius = 8
            entityService.attach(c)

        return True


class BlueCircle(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 12
        self.color = "blue"
        self.shape = "hexagon"
        self.speed = 4.35
        self.toward_range = gameState.screen["width"]
        self.points = 200

    def create(self):
        return BlueCircle()


class RedClone(Entity):
    last_shot = 0

    def init(self):
        Entity.init(self)
        self.radius = 16
        self.color = "red"
        self.shape = "ship"
        self.speed = 2.45
        self.shield = 5
        self.spin_speed = 0
        self.rotate_toward = True
        self.toward_range = gameState.screen["width"]
        self.points = 2000
        self.spawn_effect = Effects.spawn1

    def create(self):
        return RedClone()

    def update(self, dt):
        e = self
        if e.tick - (e.last_shot or 0) < 1500:
            return

        player = gameState.player
        x = player.pos.x
        y = player.pos.y
        dist = distance(x, y, e.pos.x, e.pos.y)
        enemy_range = 500

        if dist < enemy_range:
            missile = entityService.create(e.pos.x, e.pos.y, EntityType.enemyShot)
            missile.direction = Vector(
                (x - e.pos.x) / dist * missile.speed,
                (y - e.pos.y) / dist * missile.speed,
            )
            entityService.attach(missile)
            e.last_shot = e.tick


class Butterfly(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 10
        self.color = "yellow"
        self.shape = "triangle"
        self.speed = 5
        self.direction = Vector(0, 0)
        self.max_count = 60
        self.points = 300
        self.spawn_effect = Effects.spawn3

    def create(self):
        return Butterfly()


class Snake(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 16
        self.color = "magenta"
        self.polygon = 5
        self.rotate_toward = True
        self.speed = 3.5
        self.rotation = Rand(0, 360)
        self.spin_speed = 0
        self.shield = 3
        self.max_count = 12
        self.points = 1000
        self.angle_offset = 45
        self.spawn_effect = Effects.spawn1

    def create(self):
        return Snake()

    def kill(self, killer):
        Entity.kill(self, killer)
        if self.nextNode != None:
            self.nextNode.freeze = 250
            self.nextNode.headNode = None

        return True

    def update(self, dt):
        n = self
        if n.nextNode == None:
            h = n
            for i in range(0, 8 + Rand(0, 12)):
                b = entityService.create(n.pos.x, n.pos.y, EntityType.snakeBody)
                h.nextNode = b
                b.headNode = h
                entityService.attach(b)
                h = b

        dx = n.direction.x
        dy = n.direction.y
        speed = n.speed
        rot = n.rotation
        rotdir = n.rotation_dir

        dx += Cos(rot) * speed * 0.2
        dy += Sin(rot) * speed * 0.2

        if rotdir == 0:
            rot += 4 * gameState.speed_scale
        else:
            rot -= 4 * gameState.speed_scale

        if n.wall:
            rot += 90

        if Rand(1, 1000) > 90:
            rotdir = 1 - rotdir

        n.rotation = rot
        n.spin_speed = 0
        n.direction = Vector(dx, dy)


class SnakeBody(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 10
        self.color = "white"
        self.shape = "triangle"
        self.speed = 3.5
        self.rotate_toward = True
        self.spin_speed = 0
        self.max_count = 120
        self.angle_offset = 90
        self.points = 500

    def create(self):
        return SnakeBody()

    def update(self, dt):
        e = self
        h = e.headNode

        if h == None:
            if e.nextNode != None:
                e.nextNode.headNode = None
                e.nextNode.freeze = 25
            entityService.destroy(e)
            entityService.createParticles(e.pos.x, e.pos.y, 2, e.color)
            return

        dist = distance(h.pos.x, h.pos.y, e.pos.x, e.pos.y)
        mdist = (h.radius + e.radius) * 0.75

        dx = e.direction.x
        dy = e.direction.y
        hx = h.pos.x - e.pos.x
        hy = h.pos.y - e.pos.y
        if dist >= mdist:
            dx = (hx / dist) * h.speed
            dy = (hy / dist) * h.speed
        else:
            dx *= 0.5
            dy *= 0.5

        e.direction = Vector(dx, dy)

    def repel(self):
        return

    def kill(self, killer):
        entityService.createParticles(self.pos.x, self.pos.y, 3, self.color)
        return False


class LineEnd(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 12
        self.color = "blue"
        self.shape = "triangle"
        self.speed = 1.0
        self.toward_range = gameState.screen["width"]
        self.max_count = 60
        self.points = 500
        self.spawn_effect = Effects.spawn3

    def create(self):
        return LineEnd()

    def update(self, dt):
        e = self

        chain_length = 200

        # find unhinged
        if e.nextNode == None and e.headNode == None:
            for f in entityService.entities[e.type]:
                if f == e:
                    continue
                if f.headNode != None or f.nextNode != None:
                    continue
                dist = distance(f.pos.x, f.pos.y, e.pos.x, e.pos.y)
                if dist < chain_length:
                    e.nextNode = f
                    f.headNode = e
                    break

        if e.nextNode != None:
            f = e.nextNode
            v = Vector(f.pos.x - e.pos.x, f.pos.y - e.pos.y)
            v.normalize()
            v.scale(chain_length)
            f.pos = Vector.copy(e.pos)
            f.pos.x += v.x
            f.pos.y += v.y
            return

        # kill player with line

    def kill(self, killer):
        e = self
        # unhinge before killing
        if e.headNode != None:
            e.headNode.nextNode = None
            e.headNode = None
        if e.nextNode != None:
            e.nextNode.headNode = None
            e.nextNode = None
        Entity.kill(e, killer)

        return True


class Generator(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 16
        self.color = "yellow"
        self.shape = "pentagon"
        self.speed = 2
        self.spin_speed = 0.5
        self.shield = 2
        self.direction = Vector(0, 0)
        self.max_count = 8

        self.generate_what = EntityType.pinkPinwheel
        self.generate_size = 10
        self.generate_rate = 30
        self.points = 1000
        self.spawn_effect = Effects.spawn2

    def create(self):
        return Generator()

    def update(self, dt):
        e = self
        max_tick = (e.generate_rate + 42 - e.generate_size) * 10
        if (e.tick * gameState.speed_scale) / 2 > max_tick:
            e.tick = 0
            entityService.attach(
                entityService.create(
                    e.pos.x + Rand(-10, 10), e.pos.y + Rand(-10, 10), e.generate_what
                )
            )

        self.direction = Vector.identity()


class Shot(Entity):
    bouncy = False
    superShot = False

    def init(self):
        Entity.init(self)
        self.radius = 10
        self.color = "yellow"
        self.speed = gameState.speed_shot
        self.direction = Vector.identity()

    def create(self):
        return Shot()

    def bound(self):
        if self.bouncy:
            Entity.bound()
            return

        e = self
        x = e.pos.x
        y = e.pos.y
        if (
            (x < 12)
            or (x > gameState.screen["width"] - 12)
            or (y < 12)
            or (y > gameState.screen["height"] - 12)
        ):
            entityService.createParticles(x, y, Rand(1, 3), e.color)
            entityService.destroy(e)

    def repel(self):
        return

    def kill(self, killer):
        return False

    def update(self, dt):
        enemies = entityService.enemies

        e = self
        for k in enemies:
            for n in enemies[k]:
                dist = distance(n.pos.x, n.pos.y, e.pos.x, e.pos.y)
                if dist < (n.radius + e.radius):
                    if self.superShot == False:
                        entityService.destroy(e)
                    if n.shield > 0 and self.superShot == False:
                        n.shield -= 1
                    else:
                        n.kill(self)
                    return


class Bomb(Shot):
    def init(self):
        Shot.init(self)
        self.radius = 10
        self.color = "yellow"
        self.life = 2000
        self.max_count = 1
        self.polygon = 8
        self.superShot = True
        self.direction = Vector.identity()
        self.spawn_effect = Effects.explosion

    def create(self):
        return Bomb()

    def update(self, dt):
        self.radius += 20
        self.direction = Vector.identity()
        Shot.update(self, dt)


class Explosion(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 10
        self.color = "white"
        self.life = 500
        self.max_count = 20
        self.polygon = 8
        self.spin_speed = 1
        self.direction = Vector.identity()

    def create(self):
        return Explosion()

    def update(self, dt):
        self.radius += 5
        self.direction = Vector.identity()
        Entity.update(self, dt)


class EnemyShot(Shot):
    def init(self):
        Shot.init(self)
        self.freeze = 0
        self.color = "orange"
        self.radius = 10
        self.life = 2500
        self.speed = 4.45
        self.direction = Vector.identity()

    def create(self):
        return EnemyShot()

    def update(self, dt):
        e = self
        n = gameState.player
        dist = distance(n.pos.x, n.pos.y, e.pos.x, e.pos.y)
        if dist < e.radius + n.radius:
            entityService.destroy(self)
            n.kill(self)


class FloatingText(Entity):
    def init(self):
        Entity.init(self)
        self.life = 1500
        self.radius = 0
        self.direction = Vector(0, -1)
        self.max_count = 40

    def create(self):
        return FloatingText()

    def blackhole(self):
        return

    def repel(self):
        return


class EntityService:
    last_shot = 0
    entities = {}
    enemies = {}

    createParticles: any
    createFloatingText: any

    defs = {
        EntityType.pinkPinwheel: PinkPinwheel(),
        EntityType.blueDiamond: BlueDiamond(),
        EntityType.greenSquare: GreenSquare(),
        EntityType.purpleSquare: PurpleSquare(),
        EntityType.blueCircle: BlueCircle(),
        EntityType.redCircle: None,
        EntityType.lineEnd: LineEnd(),
        EntityType.snake: Snake(),
        EntityType.snakeBody: SnakeBody(),
        EntityType.redClone: RedClone(),
        EntityType.butterfly: Butterfly(),
        EntityType.generator: Generator(),
        EntityType.player: None,
        EntityType.shot: Shot(),
        EntityType.enemyShot: EnemyShot(),
        EntityType.particle: None,
        EntityType.floatingText: FloatingText(),
        EntityType.powerUp: None,
        EntityType.bomb: Bomb(),
        EntityType.explosion: Explosion(),
    }

    def init(self):
        for k in self.defs.keys():
            self.entities[k] = []
            if k in [
                EntityType.pinkPinwheel,
                EntityType.blueDiamond,
                EntityType.greenSquare,
                EntityType.purpleSquare,
                EntityType.blueCircle,
                EntityType.redCircle,
                EntityType.lineEnd,
                EntityType.snake,
                EntityType.snakeBody,
                EntityType.redClone,
                EntityType.butterfly,
                EntityType.generator,
            ]:
                self.enemies[k] = self.entities[k]

    def create(self, x, y, what, freeze=0):
        e = self.defs[what].create()
        e.init()
        e.pos = Vector(x, y)
        e.type = what
        e.freeze = freeze * 20
        return e

    def attach(self, e):
        base = self.defs[e.type]
        if base.max_count > 0 and len(self.entities[e.type]) >= base.max_count:
            return None
        self.entities[e.type].append(e)
        return e

    def destroy(self, e: Entity):
        try:
            idx = self.entities[e.type].index(e)
            if idx != -1:
                del self.entities[e.type][idx]
        except:
            # could have been removed already (like a shot's life expiriing while also killing a enemy)
            return

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
        e.angle += e.spin_speed * gameState.speed_scale
        e.pos = Vector(x, y)

        # rotate
        if e.rotate_toward:
            a = angleTo(0, 0, e.direction.x + 0.1, e.direction.y + 0.1) + 360
            e.angle += 360
            e.angle *= 4
            e.angle += a
            e.angle /= 5
            e.angle -= 360

        player = gameState.player
        e.bound()

        if not player is None and e.toward_range > 0:
            e.toward(player.pos.x, player.pos.y, e.toward_range)

        e.repel()
        e.blackhole()
        e.update(dt)
        e.damp()


entityService = EntityService()
