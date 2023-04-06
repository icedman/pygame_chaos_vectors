from enum import Enum


class Effects(Enum):
    none = 0
    shot = 1
    powerup = 2
    destroy = 3
    explosion = 4
    spawn1 = 10
    spawn2 = 11
    spawn3 = 12
    spawn4 = 13
    spawn5 = 14


class Sounds:
    defs = {}
    requests = {}

    def play(self, s):
        if not s in self.defs:
            return
        if not s in self.requests:
            self.requests[s] = 0
        self.requests[s] += 1


soundService = Sounds()
