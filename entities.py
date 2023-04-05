from state import gameState
from maths import *
from enum import Enum
from grid import grid


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

    def init(self):
        n = self
        dir = Rand(0, 359)
        mag = Rnd(2, 4)
        n.direction.x = Cos(dir) * mag
        n.direction.y = Sin(dir) * mag
        n.spin_speed = Rnd(1, 4)
        n.speed = self.speed * gameState.speed_nme

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

    def kill(self):
        e = self
        if e.points > 0:
            entityService.createFloatingText(
                e.pos.x, e.pos.y, "+{}".format(e.points), e.color
            )
        entityService.createParticles(e.pos.x, e.pos.y, 8, e.color)
        entityService.destroy(e)
        grid.pull(e.pos.x, e.pos.y, 8, 8)
        # grid.push(e.pos.x, e.pos.y, 8, 1)

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

    def blackHole(self):
        blackhole_list = entityService.entities[EntityType.redCircle]
        for blackhole in blackhole_list:
            if blackhole.size > 0:
                ddx = blackhole.pos.x - self.pos.x
                ddy = blackhole.pos.y - self.pos.y
                dist = Sqr(ddx * ddx + ddy * ddy) + 0.001
                dx = self.direction.x
                dy = self.direction.y
                if dist < 75 + blackhole.size * 8:
                    dx = dx + ddx / dist / 512 * (1200 - dist)
                    dy = dy + ddy / dist / 512 * (1200 - dist)
                    self.direction = Vector(dx, dy)
                    if dist < 12 + blackhole.size / 2:
                        self.points = 0
                        self.kill()
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

    def create(self):
        return PinkPinwheel()


class BlueDiamond(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 18
        self.color = "cyan"
        self.speed = 3.25
        self.toward_range = gameState.screen["width"]

    def create(self):
        return BlueDiamond()


class PurpleSquare(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 16
        self.color = "purple"
        self.speed = 3
        self.toward_range = gameState.screen["width"]
        self.max_count = 60

    def create(self):
        return PurpleSquare()

    def kill(self):
        e = self
        if e.radius != 16:
            Entity.kill(e)
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


class BlueCircle(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 12
        self.color = "blue"
        self.shape = "hexagon"
        self.speed = 4.35
        self.toward_range = gameState.screen["width"]

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

    def create(self):
        return Butterfly()


class Snake(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 16
        self.color = "magenta"
        self.shape = "triangle"
        self.rotate_toward = True
        self.speed = 3.5
        self.rotation = Rand(0, 360)
        self.spin_speed = 0
        self.shield = 3
        self.max_count = 12
        self.angle_offset = 90 + 180

    def create(self):
        return Snake()

    def kill(self):
        Entity.kill(self)
        if self.nextNode != None:
            self.nextNode.freeze = 250
            self.nextNode.headNode = None

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
        self.max_count = 80
        self.angle_offset = 90

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

        # vh = Vector(e.pos.x - h.pos.x, e.pos.y - h.pos.y)
        # vh.normalize()
        # e.speed = h.speed - 0.01
        # vh.scale(mdist)
        # e.direction = Vector.identity()
        # e.pos = Vector.copy(h.pos)
        # e.pos.add(vh)

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

    def kill(self):
        entityService.createParticles(self.pos.x, self.pos.y, 3, self.color)


class LineEnd(Entity):
    def init(self):
        Entity.init(self)
        self.radius = 12
        self.color = "blue"
        self.color = "triangle"
        self.speed = 1.0
        self.toward_range = gameState.screen["width"]

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

    def kill(self):
        e = self
        # unhinge before killing
        if e.headNode != None:
            e.headNode.nextNode = None
            e.headNode = None
        if e.nextNode != None:
            e.nextNode.headNode = None
            e.nextNode = None
        Entity.kill(e)


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
        self.max_count = 6

        self.generate_what = EntityType.pinkPinwheel
        self.generate_size = 10
        self.generate_rate = 30

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

    def kill(self):
        return

    def update(self, dt):
        enemies = entityService.enemies

        e = self
        for k in enemies:
            for n in enemies[k]:
                dist = distance(n.pos.x, n.pos.y, e.pos.x, e.pos.y)
                if dist < (n.radius + e.radius):
                    entityService.destroy(e)
                    if n.shield > 0:
                        n.shield -= 1
                    else:
                        n.kill()
                    return


class EnemyShot(Shot):
    def init(self):
        Entity.init(self)
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
            # print("player hit")


class FloatingText(Entity):
    def init(self):
        Entity.init(self)
        self.life = 1500
        self.radius = 0
        self.direction = Vector(0, -1)
        self.max_count = 20

    def create(self):
        return FloatingText()

    def blackHole(self):
        return

    def repel(self):
        return


class Player(Entity):
    last_direction = Vector()

    def init(self):
        Entity.init(self)
        self.radius = 16
        self.color = "white"
        self.shape = "ship"
        self.rotate_toward = True
        self.direction = Vector()

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
            my * speed_player * gameState.speed_scale,
        )
        if mx != 0 or my != 0:
            self.last_direction = Vector(mx, my)

        a = angleTo(0, 0, n.last_direction.x, n.last_direction.y) + 360
        n.angle += 360
        n.angle *= 4
        n.angle += a
        n.angle /= 5
        n.angle -= 360

        fx = 1 if (keys["right"] == True) else 0
        fx += -1 if (keys["left"] == True) else 0
        fy = 1 if (keys["down"] == True) else 0
        fy += -1 if (keys["up"] == True) else 0

        if (fx or fy) and (
            gameState.tick - entityService.last_shot
        ) > gameState.fire_rate:
            shot = entityService.create(n.pos.x, n.pos.y, EntityType.shot)
            shot.direction = Vector(fx * shot.speed, fy * shot.speed)
            entityService.last_shot = gameState.tick
            entityService.attach(shot)

    def update(self, dt):
        enemies = entityService.enemies

        e = self

        # die from enemies
        e.color = "white"
        for k in enemies:
            for n in enemies[k]:
                dist = distance(n.pos.x, n.pos.y, e.pos.x, e.pos.y)
                if dist < (n.radius + e.radius):
                    e.color = "red"
                    n.kill()
                    # print("player hit")
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
        EntityType.player: Player(),
        EntityType.shot: Shot(),
        EntityType.enemyShot: EnemyShot(),
        EntityType.particle: None,
        EntityType.floatingText: FloatingText(),
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
        self.enemies[EntityType.floatingText] = []

    def create(self, x, y, what, freeze=0):
        e = self.defs[what].create()
        e.init()
        e.pos = Vector(x, y)
        e.type = what
        e.freeze = freeze
        return e

    def attach(self, e):
        base = self.defs[e.type]
        if base.max_count > 0 and len(self.entities[e.type]) >= base.max_count:
            return
        self.entities[e.type].append(e)

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
            a = angleTo(0, 0, e.direction.x, e.direction.y) + 360
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
        e.blackHole()
        e.update(dt)
        e.damp()


entityService = EntityService()
