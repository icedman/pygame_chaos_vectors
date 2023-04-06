class GameState:
    spawn_count = [0, 0, 0, 0]
    starting_difficulty = 0

    speed_scale = 1
    speed_player = 4

    gameOver = False
    tick = 0
    screen = {"width": 1024, "height": 768}
    keys = {
        "w": False,
        "a": False,
        "s": False,
        "d": False,
        "left": False,
        "right": False,
        "up": False,
        "down": False,
    }

    speed_enemy = 0.75
    speed_shot = 8
    speed_particle = 3
    fire_rate = 100
    last_gt = 0
    spawn_gt = 0
    power_gt = 0

    player = None
    score = 0
    ships = 3
    bombs = 3
    shield = 3

    powers = {}

    def init(self):
        self.speed_scale = 1
        self.speed_player = 1.8
        self.tick = 0
        self.gameOver = False
        self.keys = {
            "w": False,
            "a": False,
            "s": False,
            "d": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }
        self.speed_enemy = 0.75
        self.speed_shot = 4
        self.speed_particle = 3
        self.fire_rate = 300
        self.last_gt = 0
        self.spawn_gt = 0
        self.power_gt = 0
        self.player = None
        self.spawn_count = [0, 0, 0, 0]
        self.score = 0
        self.ships = 3
        self.bombs = 3
        self.shield = 0
        self.powers = {}

    def multiplier(self):
        # PowerType.multiplier
        if 7 in self.powers:
            return self.powers[7] + 1
        return 1


gameState = GameState()
