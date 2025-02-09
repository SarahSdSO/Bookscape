import pygame
from states.state import State

class WinningState(State):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 50)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

    def draw(self):
        self.game.screen.fill((50, 30, 30))
        winning_text = self.font.render("Você venceu!", True, (0, 255, 0))
        self.game.screen.blit(winning_text, (self.game.WIDTH // 2 - winning_text.get_width() // 2, self.game.HEIGHT // 2 - 50))
        pygame.display.flip()