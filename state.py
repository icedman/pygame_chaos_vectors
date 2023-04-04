class GameState:
    spawn_count = [0, 0, 0, 0]
    starting_difficulty = 0

    speed_scale = 1
    speed_player = 4

    tick = 0
    cnt = 0
    screen = {"width": 1024, "height": 768}
    keys: dict[str, bool] = {
        "w": False,
        "a": False,
        "s": False,
        "d": False,
        "left": False,
        "right": False,
        "up": False,
        "down": False,
    }

    speed_nme = 0.75
    speed_shot = 8
    speed_particle = 3
    fire_rate = 100
    last_gt = 0
    spawn_gt = 0

    player = None

    def init(self):
        self.speed_scale = 1
        self.speed_player = 4
        self.tick = 0
        self.cnt = 0
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
        self.speed_nme = 0.75
        self.speed_shot = 8
        self.speed_particle = 3
        self.fire_rate = 100
        self.last_gt = 0
        self.spawn_gt = 0
        self.player = None
        self.spawn_count = [0, 0, 0, 0]


gameState = GameState()
