import pygame
from states.menuState import MenuState
from states.ticTacToeState import TicTacToeState

class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH = 1000
        self.HEIGHT = 600
        self.FPS = 60

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Bookscape")
        self.clock = pygame.time.Clock()
       
        self.heart_image = pygame.image.load("assets/backgrounds/heart.png")
        self.heart_image = pygame.transform.scale(self.heart_image, (50, 30))
        self.lives = 3
        self.running = True

        self.icon = pygame.image.load("assets/icons/gameIcon.png")
        pygame.display.set_icon(self.icon)
        
        self.state = MenuState(self)

    def change_state(self, new_state):
        self.state = new_state

    def run(self):
        while self.running:
            self.state.handle_events()
            self.state.update()
            self.state.draw()
            self.clock.tick(self.FPS)
        pygame.quit()