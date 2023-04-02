import pygame
from maths import *
from fnt import *


class ContextState:
    strokeWidth = 3
    matrix: Matrix = Matrix.identity()

    def __init__(self, copy=None):
        if copy != None:
            self.strokeWidth = copy.strokeWidth
            self.matrix = Matrix.copy(copy.matrix)


class Context:
    _states: list[ContextState] = []
    surface: any = None

    def __init__(self, surface):
        self.surface = surface
        self._states.append(ContextState())

    def save(self):
        self._states.append(ContextState(self.state))

    def restore(self):
        del self._states[len(self._states) - 1]

    def translate(self, x, y):
        m = Matrix.identity()
        m.translate(x, y, 0)
        self.state.matrix.multiply(m)

    def scale(self, x, y):
        m = Matrix.identity()
        m.scale(x, y, 1)
        self.state.matrix.multiply(m)

    def rotate(self, az):
        m = Matrix.identity()
        m.rotate(0, 0, az * 3.14 / 180)
        self.state.matrix.multiply(m)

    @property
    def state(self):
        return self._states[len(self._states) - 1]

    def clear(self, color):
        self.surface.fill(color)

    def drawLine(self, x, y, x2, y2, color):
        m = self.state.matrix
        v1 = Vector(x, y).transform(m)
        v2 = Vector(x2, y2).transform(m)
        pygame.draw.line(
            self.surface, color, [v1.x, v1.y], [v2.x, v2.y], self.state.strokeWidth
        )

    def drawRect(self, x, y, w, h, color):
        pygame.draw.rect(self.surface, color, [x, y, w, h], self.state.strokeWidth)

    def drawPolygon(self, x, y, r, sides, color):
        if sides < 3:
            return

        points = []
        for i in range(0, sides):
            angle = ((360 / sides) * i) * 3.14 / 180
            px = x + r * Cos(angle)
            py = y + r * Sin(angle)
            points.append([px, py])
        points.append(points[0])

        for i in range(1, sides + 1):
            p1 = points[i - 1]
            p2 = points[i]
            self.drawLine(p1[0], p1[1], p2[0], p2[1], color)

    def drawPolygonPoints(self, points, color):
        for i in range(1, len(points)+1):
            p1 = points[i - 1]
            k = i
            if (k == len(points)):
                k =0
            p2 = points[k]
            self.drawLine(p1[0], p1[1], p2[0], p2[1], color)

    def drawChar(self, x, y, c, size, color, extentsOnly=False):
        pts = fnt[C(c) - C(" ")]
        next_moveto = 1
        startPosition = {}

        adv = x

        for i in range(0, 8):
            delta = pts[i]
            if delta == FONT_LAST:
                break
            if delta == FONT_UP:
                next_moveto = 1
                continue

            dx = ((delta >> 4) & 0xF) * size
            dy = ((delta >> 0) & 0xF) * -size

            if next_moveto != 0:
                startPosition = {"x": x + dx, "y": y + dy}

                if x + dx > adv:
                    adv = x + dx + (size * 4)

            else:
                nextPosition = {"x": x + dx, "y": y + dy}

                if x + dx > adv:
                    adv = x + dx + (size * 4)

                if not extentsOnly:
                    self.drawLine(
                        startPosition["x"],
                        startPosition["y"],
                        nextPosition["x"],
                        nextPosition["y"],
                        color,
                    )

                startPosition = nextPosition

            next_moveto = 0

        adv -= x
        if adv < 12 * size:
            adv = 12 * size

        return adv

    def drawText(self, x, y, text, size, color, align=0):
        text = text.upper()

        adv = 0
        extents = 0

        # get extents
        for i in range(0, len(text)):
            c = text[i]
            adv = self.drawChar(x, y, c, size, color, True)
            extents += adv

        # center
        if align == 0:
            x -= extents / 2

        # right
        if align == 2:
            x -= extents

        for i in range(0, len(text)):
            c = text[i]
            adv = self.drawChar(x, y + (-size * 0.5), c, size, color, False)
            x += adv