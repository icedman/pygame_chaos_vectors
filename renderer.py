from maths import *
from game import Game
from state import gameState
from draw import Context
from entities import *
from shapes import shapes
from grid import grid


def renderPolygon(ctx: Context, sides, x, y, r, angle, color="red"):
    ctx.save()
    ctx.rotate(angle)
    ctx.scale(r, r)
    ctx.translate(x, y)
    ctx.drawPolygon(0, 0, 1, sides, color)
    ctx.restore()


def renderDefault(ctx: Context, e: Entity):
    if e.shape != "":
        sl = shapes[e.shape]["shapes"]
        ctx.drawShape(sl, e.pos.x, e.pos.y, e.radius, e.angle + e.angle_offset, e.color)
    elif e.polygon > 0:
        renderPolygon(
            ctx,
            e.polygon,
            e.pos.x,
            e.pos.y,
            e.radius,
            ((e.angle + 360 - 90) % 360),
            e.color,
        )
    elif e.radius > 0:
        renderPolygon(
            ctx, 4, e.pos.x, e.pos.y, e.radius, e.angle + e.angle_offset, e.color
        )
    if e.text != "":
        ctx.saveAttributes()
        ctx.state.strokeWidth = 1
        ctx.drawText(e.pos.x, e.pos.y, e.text, 1.5, e.color)
        ctx.restore()


def renderPowerup(ctx: Context, e: Entity):
    renderDefault(ctx, e)
    ctx.drawText(e.pos.x + 3, e.pos.y + 8, "?", 1.5, "yellow")


def renderBomb(ctx: Context, e: Entity):
    renderDefault(ctx, e)


def renderPlayer(ctx: Context, e: Entity):
    points = []
    for i in range(0, len(e.last_positions), 3):
        v = e.last_positions[i]
        points.append([v.x, v.y])
    if len(points) > 2:
        ctx.saveAttributes()
        ctx.state.strokeWidth = 3
        ctx.drawPolygonPoints(points, "orange", False)
        ctx.restore()

    renderDefault(ctx, e)
    if gameState.shield > 0:
        ctx.saveAttributes()
        t = Floor(gameState.shield if gameState.shield < 4 else 4)
        ctx.state.strokeWidth = 1 + t
        clrs = ["red", "orange", "cyan", "cyan", "cyan"]
        renderPolygon(ctx, 7, e.pos.x, e.pos.y, e.radius + 10, e.angle, clrs[t])
        ctx.restore()


def renderBlackhole(ctx: Context, e: Entity):
    renderDefault(ctx, e)
    if e.active == False:
        return

    r = e.radius
    angle = e.angle
    color = e.color
    shape = e.shape
    e.radius += Rand(e.size, e.size + 20) / 4
    if (e.radius) > 80:
        e.radius = 80
    e.angle += Rand(20, 40 + Floor(e.size / 10))
    e.color = "cyan"
    e.shape = ""
    sz = Floor(e.size / 20)
    if sz > 5:
        sz = 5
    e.polygon = 5 + sz
    renderDefault(ctx, e)
    e.radius = r
    e.angle = angle
    e.color = color
    e.shape = shape
    e.polygon = 0


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
    pp = (e.life - e.tick) / (e.life + 1)
    d.scale(e.radius + 4 * pp)
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
        EntityType.redCircle: renderBlackhole,
        EntityType.lineEnd: renderLineEnd,
        EntityType.snake: renderDefault,
        EntityType.redClone: renderDefault,
        EntityType.butterfly: renderDefault,
        EntityType.generator: renderDefault,
        EntityType.snakeBody: renderDefault,
        EntityType.player: renderPlayer,
        EntityType.shot: renderShot,
        EntityType.enemyShot: renderShot,
        EntityType.particle: renderParticle,
        EntityType.floatingText: renderDefault,
        EntityType.powerUp: renderPowerup,
        EntityType.bomb: renderBomb,
        EntityType.explosion: renderBomb,
    }

    @staticmethod
    def renderEntity(ctx: Context, e: Entity):
        r = Renderer.defs[e.type]
        r(ctx, e)


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
    ctx.save()
    ctx.scale(1, 1.05)
    ctx.state.color = (55, 55, 55)
    ctx.state.strokeWidth = 1
    renderGridDots(ctx)
    renderGridLines(ctx)
    ctx.restore()
