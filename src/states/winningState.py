import pygame
from states.state import State

class WinningState(State):
    def __init__(self, game):
        super().__init__(game)
        self.background = pygame.image.load("assets/backgrounds/win.png")
        self.background = pygame.transform.scale(self.background, (self.game.WIDTH, self.game.HEIGHT))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

    def draw(self):
        self.game.screen.blit(self.background, (0, 0))
        pygame.display.flip()