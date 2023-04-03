from maths import *
from game import Game
from state import gameState
from draw import Context
from entities import *
from shapes import shapes


def renderShape(ctx: Context, shape: str, x, y, r, color="red"):
    sl = shapes[shape]["shapes"]
    ctx.save()
    ctx.scale(r, r)
    ctx.translate(x, y)
    for s in sl:
        points = []
        for p in s["points"]:
            points.append(p)
        ctx.translate(points[0][0] * r, points[0][1] * r)
        del points[0]
        ctx.drawPolygonPoints(points, color)
    ctx.restore()


def renderEntityShape(ctx: Context, e: Entity):
    return


def renderDefault(ctx: Context, e: Entity):
    if e.radius > 0:
        ctx.save()
        ctx.rotate(e.angle)
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
