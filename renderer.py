from maths import *
from game import Game
from state import gameState
from draw import Context
from entities import *
from shapes import shapes
from grid import grid


def renderShape(ctx: Context, shape: str, x, y, r, angle, color="red"):
    sl = shapes[shape]["shapes"]
    ctx.save()
    ctx.rotate((angle + 360 - 90) % 360)
    ctx.scale(r, r)
    ctx.translate(x, y)
    for s in sl:
        if "points" in s:
            points = []
            for p in s["points"]:
                points.append(p)
            ctx.translate(points[0][0] * r, points[0][1] * r)
            del points[0]
            ctx.drawPolygonPoints(points, color)
        if "polygon" in s:
            ctx.drawPolygon(0, 0, s["scale"], s["polygon"], color)
    ctx.restore()


def renderDefault(ctx: Context, e: Entity):
    if e.shape != "":
        renderShape(
            ctx, e.shape, e.pos.x, e.pos.y, e.radius, e.angle + e.angle_offset, e.color
        )
    elif e.radius > 0:
        ctx.save()
        ctx.rotate(e.angle + e.angle_offset)
        ctx.translate(e.pos.x, e.pos.y)
        ctx.drawPolygon(0, 0, e.radius, 4, e.color)
        ctx.restore()
    if e.text != "":
        ctx.drawText(e.pos.x, e.pos.y, e.text, 2, e.color)


def renderLineEnd(ctx: Context, e: Entity):
    renderDefault(ctx, e)
    if e.headNode != None:
        return
    if e.nextNode != None:
        ctx.drawLine(e.pos.x, e.pos.y, e.nextNode.pos.x, e.nextNode.pos.y, "yellow")


def renderShot(ctx: Context, e: Entity):
    d = Vector.copy(e.direction)
    d.normalize()
    d.scale(e.radius)
    ctx.drawLine(
        e.pos.x,
        e.pos.y,
        e.pos.x + d.x,
        e.pos.y + d.y,
        e.color,
    )
    return


def renderParticle(ctx: Context, e: Entity):
    d = Vector.copy(e.direction)
    d.normalize()
    d.scale(2)
    ctx.drawLine(
        e.pos.x,
        e.pos.y,
        e.pos.x + d.x,
        e.pos.y + d.y,
        e.color,
    )
    return


class Renderer:
    defs: dict[EntityType, any] = {
        EntityType.pinkPinwheel: renderDefault,
        EntityType.blueDiamond: renderDefault,
        EntityType.greenSquare: renderDefault,
        EntityType.purpleSquare: renderDefault,
        EntityType.blueCircle: renderDefault,
        EntityType.redCircle: renderDefault,
        EntityType.lineEnd: renderLineEnd,
        EntityType.snake: renderDefault,
        EntityType.redClone: renderDefault,
        EntityType.butterfly: renderDefault,
        EntityType.generator: renderDefault,
        EntityType.snakeBody: renderDefault,
        EntityType.player: renderDefault,
        EntityType.shot: renderShot,
        EntityType.enemyShot: renderShot,
        EntityType.particle: renderParticle,
        EntityType.floatingText: renderDefault,
    }

    @staticmethod
    def renderEntity(ctx: Context, e: Entity):
        r = Renderer.defs[e.type]
        r(ctx, e)

        if e.text != "":
            ctx.drawText(e.pos.x, e.pos.y, e.text, 2, e.color)


def renderGridDots(ctx):
    for c in grid.grid:
        for r in c:
            ctx.drawLine(r.x, r.y, r.x - 1, r.y - 1)


def renderGridLines(ctx):
    rc = len(grid.grid)
    cc = len(grid.grid[0])

    # vertical
    for ir in range(0, rc):
        prev = None
        for ic in range(0, cc):
            r = grid.grid[ir][ic]
            if prev != None:
                ctx.drawLine(r.x, r.y, prev.x, prev.y)
            prev = r

    # horizontal
    for ic in range(0, cc):
        prev = None
        for ir in range(0, rc):
            r = grid.grid[ir][ic]
            if prev != None:
                ctx.drawLine(r.x, r.y, prev.x, prev.y)
            prev = r


def renderGrid(ctx):
    ctx.saveAttributes()
    ctx.state.color = (50, 50, 50)
    ctx.state.strokeWidth = 1
    # renderGridDots(ctx)
    renderGridLines(ctx)
    ctx.restore()
