import pygame
from states.state import State
from states.quizState import QuizState

class StoryState(State):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 30)
        self.next_button = pygame.Rect(self.game.WIDTH // 2 - 100, self.game.HEIGHT - 150, 200, 100)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.next_button.collidepoint(event.pos):
                    self.game.change_state(QuizState(self.game))

    def draw(self):
        self.game.screen.fill((50, 30, 30))
        story_text = self.font.render("Esta é a história do jogo...", True, (255, 255, 255))
        self.game.screen.blit(story_text, (self.game.WIDTH // 2 - story_text.get_width() // 2, self.game.HEIGHT // 2 - 50))
        pygame.draw.rect(self.game.screen, (87, 31, 28), self.next_button)
        next_text = self.font.render("Next", True, (255, 255, 255))
        self.game.screen.blit(next_text, (self.next_button.x + 50, self.next_button.y + 30))
        pygame.display.flip()