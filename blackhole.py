from entities import entityService, Entity, EntityType
from state import gameState
from grid import grid
from maths import *
from sounds import soundService, Effects


class RedCircle(Entity):
    size = 10
    absorbed = 0
    active = False

    def init(self):
        Entity.init(self)
        self.radius = 16
        self.color = "red"
        self.shape = "pentagon"
        self.speed = 2.5
        self.direction = Vector(0, 0)
        self.shield = 0
        self.max_count = 6
        self.points = 1000
        self.spawn_effect = Effects.spawn2

    def create(self):
        return RedCircle()

    def update(self, dt):
        speedScale = 1

        #   if (move > 0):
        #     move = move -1 * speedScale
        #     return

        px = gameState.player.pos.x
        py = gameState.player.pos.y

        x = self.pos.x
        y = self.pos.y
        dx = self.direction.x
        dy = self.direction.y

        sz = self.size

        self.angle += 1
        if self.angle > 360:
            self.angle = 0
        r = Floor(self.angle)

        x = x + dx * speedScale
        y = y + dy * speedScale

        #   gcenterx = x+Sin(r*3)*sz/2.5
        #   gcentery = y+Cos(r*3)*sz/2.5

        if self.active:
            grid.pull(x, y, (int)(sz / 12))

        #   DoubleSun()

        distx = x - px
        disty = y - py
        dist = distx * distx + disty * disty

        if dist < (12 + sz / 2) * (12 + sz / 2) + 12 * 12:
            n.kill(self)

        if self.active and r % 2 == 0:
            pp = Rand(0, 60)
            parts = entityService.createParticles(
                x + Sin(r) * (10 + sz * 1.1) + Sin(r + pp * 45) * 3,
                y + Cos(r) * (10 + sz * 1.1) + Cos(r + pp * 45) * 3,
                1,
                (150 + Rand(0, 100), 150 + Rand(0, 100), 150 + Rand(0, 100)),
                7,
                r + pp * 45,
            )
            for p in parts:
                p.speed = 2
                p.life = 2000
                p.direction.normalize()
                p.direction.scale(2)

        self.pos = Vector(x + 0, y + 0)
        self.direction = Vector(dx + 0, dy + 0)

    def kill(self, killer):
        if self.active == False:
            self.active = True
            self.shield = 5
            return False

        self.size *= 0.85
        if self.size < 0.5 or killer.type == EntityType.bomb:
            Entity.kill(self, killer)
            entityService.attach(
                entityService.create(self.pos.x, self.pos.y, EntityType.explosion)
            )
            return True

        grid.push(self.pos.x, self.pos.y, 6, 1)
        return False

    def grow(self, amnt):
        self.absorbed += 1
        speedup = 1 + (gameState.tick / (50 * 60 * 6))
        # 'increase by 1 every 6 minutes;

        sz = self.size
        if speedup > 5:
            speedup = 5
        sz = sz + amnt * speedup
        # rate = sz / 16

        self.size = sz

        grid.push(self.pos.x, self.pos.y, 6, 1)

        if sz > 50:
            if self.speed > 0.5:
                self.speed = 0.5

        if sz > 200:
            self.explode()

    def explode(self):
        for t in range(0, 16):
            xx = self.pos.x + Cos(t * 22) * 20
            yy = self.pos.y + Sin(t * 22) * 20
            entityService.attach(entityService.create(xx, yy, EntityType.purpleSquare))

        for t in range(0, 16):
            xx = self.pos.x + Cos(t * 22) * 30
            yy = self.pos.y + Sin(t * 22) * 30
            entityService.attach(entityService.create(xx, yy, EntityType.butterfly))

        entityService.destroy(self)
        soundService.play(Effects.explosion)
        grid.push(self.pos.x, self.pos.y, 8, 4)

    def blackhole(self):
        return


def pullParticles(gt):
    speedScale = 1
    st = gt % 2
    spin = 3

    if st == 0:
        spin = -3

    blackhole_list = entityService.entities[EntityType.redCircle]
    particle_list = entityService.entities[EntityType.particle]
    for blackhole in blackhole_list:
        if blackhole.size == 0:
            continue

        for t in range(0, len(particle_list), 2):
            p = particle_list[t]
            ddx = blackhole.pos.x - p.pos.x
            ddy = blackhole.pos.y - p.pos.y
            dist = Sqr(ddx * ddx + ddy * ddy)

            if dist < blackhole.size * 8 and dist > 8:
                if dist < blackhole.size / 4:
                    ddx = -ddx / dist
                    ddy = -ddy / dist
                    p.direction.x = p.direction.x + ddx / 4  # .75f
                    p.direction.y = p.direction.y + ddy / 4  # .75f
                    p.direction.x = p.direction.x + ddy / spin  # .75' / dist/4
                    p.direction.y = p.direction.y - ddx / spin  # .75' / dist/4
                else:
                    p.life += 3 * speedScale
                    ddx = ddx / dist
                    ddy = ddy / dist
                    p.direction.x = p.direction.x + ddx / 4  # .75f
                    p.direction.y = p.direction.y + ddy / 4  # .75f
                    p.direction.x = p.direction.x - ddy / spin  # .75' / dist/4
                    p.direction.y = p.direction.y + ddx / spin  # .75' / dist/4

                speed = p.direction.x * p.direction.x + p.direction.y * p.direction.y

                if speed > 12 * 12:
                    sproot = Sqr(speed)
                    p.direction.x = p.direction.x / sproot
                    p.direction.y = p.direction.y / sproot
