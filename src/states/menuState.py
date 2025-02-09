import pygame
from states.state import State
from states.storyState import StoryState

class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 50)
        self.title_font = pygame.font.Font("assets/fonts/Hestrial.ttf", 80)
        self.start_button = pygame.Rect(self.game.WIDTH // 2 - 100, self.game.HEIGHT // 2 + 95, 200, 100)
        self.button_color = (255, 255, 255)
        
        self.WIDTH = 1000
        self.HEIGHT = 600
        self.background = pygame.image.load("assets/backgrounds/menu.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        pygame.mixer.init()
        pygame.mixer.music.load("assets/music/menuSound.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.start_button.collidepoint(mouse_pos):
            self.button_color = (200, 200, 200)
        else:
            self.button_color = (255, 255, 255)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.start_button.collidepoint(event.pos):
                    self.game.change_state(StoryState(self.game))

    def draw(self):
        self.game.screen.blit(self.background, (0, 0))
        title_text = self.title_font.render("Bookscape", True, (211, 144, 137))
        self.game.screen.blit(title_text, (self.WIDTH // 2 - title_text.get_width() // 2, 130))
        start_text = self.font.render("Jogar", True, self.button_color)
        self.game.screen.blit(start_text, (self.start_button.x + 25, self.start_button.y + 25))
        pygame.display.flip()
