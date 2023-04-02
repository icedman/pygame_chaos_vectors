class GameState:
    speed_scale = 1
    speed_player = 2

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
    speed_shot = 4
    speed_particle = 3
    fire_rate = 200
    last_gt = 0

    player = None

    def init(self):
        speed_scale = 0.2
        speed_player = 10
        tick = 0
        cnt = 0
        keys = {}
        speed_nme = 0.75
        speed_shot = 4
        speed_particle = 3
        fire_rate = 200
        last_gt = 0
        player = None
        return


gameState = GameState()
