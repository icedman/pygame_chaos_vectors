from maths import *


class GridPoint:
    ox = 0
    oy = 0
    x = 0
    y = 0
    dx = 0
    dy = 0
    fx = 0
    fy = 0

    def update(self, dt, xx, yy):
        speedScale = 1

        if Abs(xx - self.x) > 2:
            self.dx += Sgn(xx - self.x)
        if Abs(yy - self.y) > 2:
            self.dy += Sgn(yy - self.y)

        if Abs(self.ox - self.x) > 1:
            self.x = self.x + Sgn(self.ox - self.x) * speedScale
            self.dx += Sgn(self.ox - self.x) / 2
        else:
            self.x = self.ox

        if Abs(self.oy - self.y) > 1:
            self.y = self.y + Sgn(self.oy - self.y) * speedScale
            self.dy += Sgn(self.oy - self.y) / 2
        else:
            self.y = self.oy

        self.dx = self.dx * 0.899
        self.dy = self.dy * 0.899

        self.x = self.x + self.dx * speedScale
        self.y = self.y + self.dy * speedScale

    def disrupt(self, xx, yy):
        if Abs(xx) > 8:
            xx = xx / 16
        if Abs(yy) > 8:
            yy = yy / 16
        self.dx = self.dx + xx
        self.dy = self.dy + yy
        self.speed = self.dx * self.dx + self.dy * self.dy
        if self.speed > 160:
            self.dx = self.dx / self.speed * 128
            self.dy = self.dy / self.speed * 128


class GridLine:
    p1: Vector = Vector()
    p2: Vector = Vector()

    def __init__(self, p1, p2):
        self.p1 = Vector.copy(p1)
        self.p2 = Vector.copy(p2)


class Grid:
    grid: list[list[GridPoint, GridPoint]] = []
    lines: list[GridLine] = []

    SCREENW = 1024
    SCREENH = 768
    PLAYFIELDW = 1024
    PLAYFIELDH = 768
    GRIDWIDTH = 16 * 4
    GRIDHEIGHT = 16 * 4
    NUMGPOINTSW = 0
    NUMGPOINTSH = 0

    def init(self, w=0, h=0):
        if w > 0 and h > 0:
            self.PLAYFIELDW = w
            self.PLAYFIELDH = h

        self.NUMGPOINTSW = Floor(1 + self.PLAYFIELDW / self.GRIDWIDTH)
        self.NUMGPOINTSH = Floor(1 + self.PLAYFIELDH / self.GRIDHEIGHT)

        for r in range(0, self.NUMGPOINTSW):
            row = []
            for c in range(0, self.NUMGPOINTSH):
                row.append(GridPoint())
            self.grid.append(row)

        self.reset()

    def update(self, dt):
        grid = self.grid
        for a in range(1, self.NUMGPOINTSW - 1):
            for b in range(1, self.NUMGPOINTSH - 1):
                xx = 0
                xx += grid[a - 1][b].x
                xx += grid[a][b - 1].x
                xx += grid[a][b + 1].x
                xx += grid[a + 1][b].x
                xx = xx / 4

                yy = 0
                yy += grid[a - 1][b].y
                yy += grid[a][b - 1].y
                yy += grid[a][b + 1].y
                yy += grid[a + 1][b].y
                yy = yy / 4

                grid[a][b].update(dt, xx, yy)

    def reset(self):
        grid = self.grid
        for a in range(0, self.NUMGPOINTSW):
            for b in range(0, self.NUMGPOINTSH):
                grid[a][b].ox = a * self.GRIDWIDTH
                grid[a][b].oy = b * self.GRIDHEIGHT
                grid[a][b].x = a * self.GRIDWIDTH
                grid[a][b].y = b * self.GRIDHEIGHT
                grid[a][b].dx = 0
                grid[a][b].dy = 0

    def pull(self, x1, y1, sz=4, amnt=4):
        grid = self.grid
        # amnt *= speedScale
        a = x1 / self.GRIDWIDTH
        b = y1 / self.GRIDHEIGHT
        for xx in range(-sz, sz):
            for yy in range(-sz, sz):
                ix = Floor(a + xx)
                iy = Floor(b + yy)
                if ix <= 0:
                    continue
                if ix < self.NUMGPOINTSW:  #'-2
                    if iy <= 0:
                        continue
                    if iy < self.NUMGPOINTSH:  #'-2
                        if xx * xx + yy * yy < sz * sz:
                            diffx = grid[ix][iy].x - x1
                            diffy = grid[ix][iy].y - y1
                            dist = Sqr(diffx * diffx + diffy * diffy)
                            if dist > 0:
                                grid[ix][iy].dx -= (
                                    diffx / dist * amnt
                                )  # '*(1-(dist*dist)/(sz*sz*4*256))
                                grid[ix][iy].dy -= (
                                    diffy / dist * amnt
                                )  # '*(1-(dist*dist)/(sz*sz*4*256))

    def push(self, x1, y1, sz=4, amnt=1):
        grid = self.grid
        # amnt *= speedScale
        a = x1 / self.GRIDWIDTH
        b = y1 / self.GRIDHEIGHT
        for xx in range(-sz, sz):
            for yy in range(-sz, sz):
                ix = Floor(a + xx)
                iy = Floor(b + yy)
                if ix <= 0:
                    continue
                if ix < self.NUMGPOINTSW:  # '-2
                    if iy <= 0:
                        continue
                    if iy < self.NUMGPOINTSH:  # '-2
                        diffx = grid[ix][iy].ox - x1
                        diffy = grid[ix][iy].oy - y1
                        diffxo = grid[ix][iy].ox - grid[ix][iy].x
                        diffyo = grid[ix][iy].oy - grid[ix][iy].y
                        dist = diffy * diffy + diffx * diffx
                        disto = diffyo * diffyo + diffxo * diffxo
                        if dist > 1 and disto < 400 and dist < 50 * 50:
                            grid[ix][iy].dx += diffx * amnt  # '/dist*amnt
                            grid[ix][iy].dy += diffy * amnt  # '/dist*amnt


grid = Grid()
