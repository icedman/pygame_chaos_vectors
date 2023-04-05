from entities import entityService, Entity, EntityType
from state import gameState
from grid import grid
from maths import *


class RedCircle(Entity):
    size = 50
    absorbed = 0

    def init(self):
        Entity.init(self)
        self.radius = 16
        self.color = "red"
        self.shape = "pentagon"
        self.speed = 2.5
        self.direction = Vector(0, 0)
        self.max_count = 6

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

        #   // radius = 12 + (sz/2)

        #   gcenterx = x+Sin(r*3)*sz/2.5
        #   gcentery = y+Cos(r*3)*sz/2.5

        if sz > 0:
            grid.pull(x, y, (int)(sz / 12))
            # '/3)

        #   DoubleSun()

        distx = x - px
        disty = y - py
        dist = distx * distx + disty * disty

        # if dist < (12 + sz / 2) * (12 + sz / 2) + 12 * 12:
        # killer = true;

        # if (KillPlayer()) {
        #   // nme5_list.Remove(this);
        #   Remove();
        # }

        # if (active):

        if sz > 0 and r % 4 == 0:
            pp = Rand(0, 60)
            parts = entityService.createParticles(
                x + Sin(r) * sz * 1.15 + Sin(r + pp * 45) * 3,
                y + Cos(r) * sz * 1.15 + Cos(r + pp * 45) * 3,
                1,
                "pink",
                7,
                r + pp * 45,
            )
            for p in parts:
                p.speed = 2
                # p.life = 2000
                p.direction.normalize()
                p.direction.scale(2)

        self.pos = Vector(x, y)
        self.direction = Vector(dx, dy)

    def kill(self):
        if self.size == 0:
            self.size = 10

    def grow(self, amt):
        self.absorbed += 1
        return

    def blackHole(self):
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
                    p.direction.x = p.direction.x + ddx / 2  # .75f
                    p.direction.y = p.direction.y + ddy / 2  # .75f
                    p.direction.x = p.direction.x + ddy / spin  # .75' / dist/4
                    p.direction.y = p.direction.y - ddx / spin  # .75' / dist/4
                else:
                    p.life += 3 * speedScale
                    ddx = ddx / dist
                    ddy = ddy / dist
                    p.direction.x = p.direction.x + ddx / 2  # .75f
                    p.direction.y = p.direction.y + ddy / 2  # .75f
                    p.direction.x = p.direction.x - ddy / spin  # .75' / dist/4
                    p.direction.y = p.direction.y + ddx / spin  # .75' / dist/4

                speed = p.direction.x * p.direction.x + p.direction.y * p.direction.y

                if speed > 12 * 12:
                    sproot = Sqr(speed)
                    p.direction.x = p.direction.x / sproot
                    p.direction.y = p.direction.y / sproot
