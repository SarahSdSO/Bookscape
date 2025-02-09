import pygame
from states.state import State
from states.storyState import StoryState

class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 50)
        self.start_button = pygame.Rect(self.game.WIDTH // 2 - 100, self.game.HEIGHT // 2 - 50, 200, 100)

        self.WIDTH = 1000
        self.HEIGHT = 600
        self.background = pygame.image.load("assets/backgrounds/menu.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.start_button.collidepoint(event.pos):
                    self.game.change_state(StoryState(self.game))

    def draw(self):
        self.game.screen.blit(self.background, (0, 0))
        pygame.draw.rect(self.game.screen, (87, 31, 28), self.start_button)
        start_text = self.font.render("Start", True, (255, 255, 255))
        self.game.screen.blit(start_text, (self.start_button.x + 50, self.start_button.y + 30))
        pygame.display.flip()