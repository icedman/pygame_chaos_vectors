from state import gameState
from entities import entityService, EntityType
import particles


class Game:
    def setup(self, size):
        gameState.screen["width"] = size[0]
        gameState.screen["height"] = size[1]
        self.newGame()

    def newGame(self):
        gameState.init()
        entityService.init()
        gameState.player = entityService.create(0, 0, EntityType.player)
        entityService.attach(gameState.player)

        # entityService.attach(entityService.create(100, 100, EntityType.pinkPinwheel))
        # entityService.attach(entityService.create(100, 100, EntityType.greenSquare))
        # entityService.attach(entityService.create(100, 100, EntityType.blueCircle))
        # entityService.attach(entityService.create(100, 100, EntityType.purpleSquare))
        # entityService.attach(entityService.create(100, 100, EntityType.snake))
        entityService.attach(entityService.create(100, 100, EntityType.redClone))

        self.centerPlayer()

    def centerPlayer(self):
        gameState.player.pos.x = gameState.screen["width"] / 2
        gameState.player.pos.y = gameState.screen["height"] / 2

    def entities(self):
        return entityService.entities

    def update(self, dt):
        gameState.tick += dt

        entities = self.entities()
        for k in entities.keys():
            ek = entities[k]
            for e in ek:
                entityService.update(e, dt)

        # gameService.spawn(gameState.tick/2);
