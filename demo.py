from scene import *
from maths import *
from draw import Context
from renderer import *
from scene import *
from state import *


class Frame(Scene):
    entered = False
    ticks = 0
    frameTicks = 0
    text = ""
    textOpts = {}
    start = None
    length = 2000
    opts = {}

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
            vdir = Vector.fromAngle(Rand(0, 360)).scale(50)
            v2 = Vector.copy(v1).add(vdir)
            self.lines.append([v1, v2])

    def onUpdate(self, dt):
        pass

    def onRender(self, gfx):
        gfx.saveAttributes()
        gfx.state.strokeWidth = 4
        for l in self.lines:
            gfx.drawLine(l[0].x, l[0].y, l[1].x, l[1].y, "white")
        gfx.restore()
        Frame.onRender(self, gfx)


class DemoScene(Scene):
    ticks = 0
    rendered = 0
    frames = []

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

        frames = _.getFrames(_.ticks)
        for f in frames:
            if f.entered:
                f.onRender(gfx)

        gfx.restore()

        self.rendered += 1
        if self.rendered > 0:
            fps = "{}fps".format(Floor(self.rendered * 1000 / self.ticks))
            gfx.drawText(80, 40, fps, 2, "red")

    def onEnter(self):
        _ = self
        _.frames = []
        # _.frames.append(Frame(2000, "hello word"))
        _.frames.append(
            FrameRandomLines(
                30000, "Draw Lines", None, {"color": "red", "align": "bottom"}
            )
        )
