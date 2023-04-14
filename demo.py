from scene import *
from maths import *
from draw import Context
from renderer import *
from scene import *
from state import *
from grid import *
from shapes import *
from entities import *


class Frame(Scene):
    entered = False
    ticks = 0
    frameTicks = 0
    text = ""
    textOpts = {}
    start = None
    length = 2000
    opts = {}

    grid = Grid()

    def __init__(self, length, text="", start=None, textOpts=None):
        _ = self
        _.ticks = 0
        _.frameTicks = 0
        _.length = length
        if text != None:
            _.text = text
        if start != None:
            _.start = start
        _.textOpts = {"size": 2, "color": "yellow", "align": "center"}
        if textOpts != None:
            for t in textOpts:
                _.textOpts[t] = textOpts[t]

        self.opts = {}

    def onEnter(self):
        pass

    def onUpdate(self, dt):
        pass

    def onRender(self, gfx):
        size = [gameState.screenWidth, gameState.screenHeight]
        tt = self.text.split("\n")
        y = 0

        gfx.saveAttributes()
        if self.textOpts["size"] > 2:
            gfx.state.strokeWidth = 3
        for t in tt:
            yy = size[1] / 2 - 40 + y
            if self.textOpts["align"] == "bottom":
                yy = size[1] - 80 + y
            gfx.drawText(size[0] / 2, yy, t, self.textOpts["size"], "yellow")
            y += 32
        gfx.restore()


class FrameRandomLines(Frame):
    lines = []

    def onEnter(self):
        size = [gameState.screenWidth, gameState.screenHeight]
        for i in range(0, 2000):
            v1 = Vector(Rand(0, size[0]), Rand(0, size[1]))
            vdir = Vector.fromAngle(Rand(0, 360)).scale(Rand(50, 80))
            v2 = Vector.copy(v1).add(vdir)
            self.lines.append([v1, v2])

    def onUpdate(self, dt):
        pass

    def onRender(self, gfx):
        gfx.saveAttributes()
        gfx.state.strokeWidth = 1
        p = self.ticks / 20 / self.length
        for i in range(0, Floor(len(self.lines) * p) - 1):
            l = self.lines[i]
            gfx.drawLine(l[0].x, l[0].y, l[1].x, l[1].y, "white")
        gfx.restore()
        Frame.onRender(self, gfx)


class FrameRandomPolygons(Frame):
    polygons = []

    def onEnter(self):
        size = [gameState.screenWidth, gameState.screenHeight]
        for i in range(0, 2000):
            v1 = Vector(Rand(0, size[0]), Rand(0, size[1]))
            # vdir = Vector.fromAngle(Rand(0, 360)).scale(50)
            # v2 = Vector.copy(v1).add(vdir)
            # self.lines.append([v1, v2])
            self.polygons.append(
                {"pos": v1, "sides": Rand(3, 8), "radius": Rand(20, 60)}
            )

    def onUpdate(self, dt):
        pass

    def onRender(self, gfx):
        gfx.saveAttributes()
        gfx.state.strokeWidth = 1
        p = self.ticks / 20 / self.length
        for i in range(0, Floor(len(self.polygons) * p) - 1):
            l = self.polygons[i]
            gfx.drawPolygon(l["pos"].x, l["pos"].y, l["radius"], l["sides"], "white")
        gfx.restore()
        Frame.onRender(self, gfx)


class FrameRandomShapes(Frame):
    polygons = []
    rot = 0

    def onEnter(self):
        size = [gameState.screenWidth, gameState.screenHeight]
        keys = []
        for k in shapes:
            keys.append(k)
        for i in range(0, 2000):
            v1 = Vector(Rand(0, size[0]), Rand(0, size[1]))
            self.polygons.append(
                {
                    "pos": v1,
                    "sides": Rand(3, 8),
                    "radius": Rand(10, 40),
                    "shape": keys[Rand(0, len(keys) - 1)],
                }
            )

    def onUpdate(self, dt):
        if self.ticks > 4000:
            self.text = ""
        if self.ticks > 5000:
            self.rot += dt
            self.text = "rotation, scale, translation matrices\ntransform their points"

    def onRender(self, gfx):
        gfx.saveAttributes()
        gfx.state.strokeWidth = 1
        p = self.ticks / 20 / self.length
        angle = (self.rot / 10) % 360
        # drawShape(self, shapes, x, y, r, angle, color="red", matrix=None)
        for i in range(0, Floor(len(self.polygons) * p) - 1):
            l = self.polygons[i]
            sl = shapes[l["shape"]]["shapes"]
            gfx.drawShape(sl, l["pos"].x, l["pos"].y, l["radius"], angle, "white")
            for s in sl:
                if "polygon" in s:
                    gfx.save()
                    gfx.rotate(angle)
                    gfx.translate(l["pos"].x, l["pos"].y)
                    gfx.drawPolygon(0, 0, l["radius"], s["polygon"], "white")
                    gfx.restore()
        gfx.restore()
        Frame.onRender(self, gfx)


game = Game()


class FrameGame(Frame):
    def onEnter(self):
        size = [gameState.screenWidth, gameState.screenHeight]
        game.setup(size)
        game.newGame()

    def onUpdate(self, dt):
        game.update(dt)

        if self.ticks > 2000:
            self.text = "In this game you evade and shoot down enemies"
        if self.ticks > 5000:
            self.text = ""
        if self.ticks > 8000:
            self.text = "They spawn and move at increase rates and speeds"
        if self.ticks > 12000:
            self.text = ""
        if self.ticks > 15000:
            self.text = "Collect power-ups to upgrade your ship and weapons"

    def onRender(self, gfx):
        Frame.onRender(self, gfx)
        entities = entityService.entities
        for k in entities.keys():
            ek = entities[k]
            for e in ek:
                Renderer.renderEntity(gfx, e)


class FrameGame2(FrameGame):
    type = EntityType.player

    def onEnter(self):
        for et in entityService.enemies:
            for n in entityService.entities[et]:
                entityService.destroy(n)

    def onUpdate(self, dt):
        game.update(dt)
        gameState.player.shield = 2
        size = [gameState.screenWidth, gameState.screenHeight]
        gameState.player.pos = Vector(size[0] / 2, size[1] / 2)
        if self.type != None:
            for et in entityService.enemies:
                if self.type == et:
                    continue
                for n in entityService.entities[et]:
                    entityService.destroy(n)

    def spawnRandom(self, t):
        size = [gameState.screenWidth, gameState.screenHeight]
        v = (
            Vector.fromAngle(Rand(0, 360))
            .scale(Rand(400, 600))
            .add(Vector(gameState.player.pos.x, gameState.player.pos.y))
        )
        e = entityService.create(v.x, v.y, t)
        entityService.attach(e)


class FrameGamePinWheel(FrameGame2):
    type = EntityType.pinkPinwheel
    count = 4

    def onEnter(self):
        FrameGame.onEnter(self)
        for i in range(0, self.count):
            self.spawnRandom(self.type)

        for i in range(0, 20):
            game.update(15)


class FrameGameGreen(FrameGamePinWheel):
    type = EntityType.greenSquare
    count = 6


class FrameGameClone(FrameGamePinWheel):
    type = EntityType.redClone
    count = 2


class FrameType(Frame):
    oText = ""

    def onEnter(self):
        self.oText = self.text

    def onUpdate(self, dt):
        p = Floor(self.ticks / (self.length - 4000) * len(self.oText))
        self.text = self.oText[0:p]
        Frame.onUpdate(self, dt)


class DemoScene(Scene):
    ticks = 0
    rendered = 0
    frames = []
    grid_gt = 0

    def onExit(self):
        pass

    def getFrames(self, ticks):
        res = []
        totalLength = 0
        for f in self.frames:
            if f.start != None:
                if ticks >= f.start and ticks < f.start + f.length:
                    f.frameTicks = f.ticks + f.start
                    res.append(f)
                continue
            s = totalLength
            if ticks >= s and ticks < s + f.length:
                f.frameTicks = f.ticks + s
                res.append(f)
            totalLength += f.length
        return res

    def onUpdate(self, dt):
        _ = self
        if gameState.released["escape"]:
            # sceneService.enterScene(SceneType.menu)
            gameState.done = True
            return

        size = [gameState.screenWidth, gameState.screenHeight]
        self.grid_gt += 1
        if self.grid_gt % 60 == 0:
            if RndOr(0, 1) == 0:
                grid.push(Rand(0, size[0]), Rand(0, size[1]), 6, 1 + Rand(0, 2))
            else:
                grid.pull(Rand(0, size[0]), Rand(0, size[1]), 8, 6 + Rand(0, 4))
        grid.update(dt)

        frames = _.getFrames(_.ticks)
        for f in frames:
            if not f.entered:
                f.onEnter()
                f.entered = True
            f.ticks += dt
            f.onUpdate(dt)

        _.ticks += dt

    def onRender(self, gfx):
        _ = self

        gfx.save()
        gfx.clear("black")

        renderGrid(gfx)

        frames = _.getFrames(_.ticks)
        for f in frames:
            if f.entered:
                f.onRender(gfx)

        gfx.restore()

        # self.rendered += 1
        # if self.rendered > 0:
        #     fps = "{}fps".format(Floor(self.rendered * 1000 / self.ticks))
        #     gfx.drawText(80, 40, fps, 2, "red")

    def onEnter(self):
        _ = self
        _.frames = []
        _.frames.append(Frame(10000))
        _.frames.append(Frame(4000, "Chaos Vectors", None, {"size": 3}))
        _.frames.append(
            Frame(4000, "A recreation of Mark Incitti's\nBlitzBasic game\nGridWars")
        )
        _.frames.append(
            Frame(
                5000,
                "Most of the algorithm and gameplay are copied\nfrom his original code\nhttps://github.com/mmatyas/GridWars",
            )
        )
        _.frames.append(
            FrameRandomLines(
                4000,
                "Every element is drawn using only calls to\nDRAW_LINE",
                None,
                {"color": "red", "align": "bottom"},
            )
        )
        _.frames.append(Frame(500))
        _.frames.append(
            FrameRandomPolygons(
                4000,
                "From lines to polygons with sides and radiuses",
                None,
                {"color": "red", "align": "bottom"},
            )
        )
        _.frames.append(Frame(500))
        _.frames.append(
            FrameRandomShapes(
                10000,
                "To vector shapes with predefined points",
                None,
                {"color": "red", "align": "bottom"},
            )
        )
        _.frames.append(Frame(500))
        _.frames.append(
            FrameType(
                8000,
                "Even this text is rendered using DRAW_LINE",
                None,
                {"color": "red", "align": "center"},
            )
        )
        _.frames.append(Frame(1000))
        _.frames.append(FrameGame(22000, "", None, {"color": "red", "align": "bottom"}))
        _.frames.append(FrameGame(1000, "", None, {"color": "red", "align": "bottom"}))
        _.frames.append(
            FrameGame2(
                2000, "Enemies are varied", None, {"color": "red", "align": "bottom"}
            )
        )
        _.frames.append(
            FrameGamePinWheel(
                6000, "Some wander around", None, {"color": "red", "align": "bottom"}
            )
        )
        _.frames.append(
            FrameGameGreen(
                6000, "Some chase you", None, {"color": "red", "align": "bottom"}
            )
        )
        _.frames.append(
            FrameGameClone(
                6000, "Some shoot at you", None, {"color": "red", "align": "bottom"}
            )
        )
        _.frames.append(Frame(1000))
        _.frames.append(Frame(4000, "Discover more enemies the longer you survive"))
        _.frames.append(Frame(5000, "How long will you last?"))
        _.frames.append(Frame(1000))
