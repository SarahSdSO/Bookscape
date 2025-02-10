import pygame
import json
from states.state import State
from states.crosswordsState import CrosswordsState
from states.gameOverState import GameOverState

class QuizState(State):
    def __init__(self, game):
        super().__init__(game)
        self.WIDTH = 1000
        self.HEIGHT = 600
        self.background = pygame.image.load("assets/backgrounds/background.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        self.font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 25)
        self.load_questions()
        self.current_question = 0
        self.time_left = 40 * self.game.FPS

    def load_questions(self):
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            self.questions = data["question"]
            self.answers = data["answer"]
            self.options = data["options"]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.check_answer(event.pos)

    def check_answer(self, mouse_pos):
        button_radius = 30  # Mantemos o raio maior para melhorar a detecção
        spacing = 65  # Ajustamos o espaçamento para corresponder ao desenho

        for i in range(len(self.options[self.current_question])):
            y_position = 280 + i * spacing  # Define a posição do botão
            button_center = (70, y_position)

            distance = ((mouse_pos[0] - button_center[0])**2 + (mouse_pos[1] - button_center[1])**2) ** 0.5
            if distance <= button_radius:
                if i == self.answers[self.current_question] - 1:
                    self.current_question += 1
                    self.time_left = 40 * self.game.FPS
                    if self.current_question == len(self.questions):
                        self.game.change_state(CrosswordsState(self.game))

                else:
                    self.game.lives -= 1
                    if self.game.lives == 0:
                        self.game.change_state(GameOverState(self.game))
                return  

    def update(self):
        if self.time_left > 0:
            self.time_left -= 1
        else:
            self.game.lives -= 1

            if self.game.lives == 0:
                self.game.change_state(GameOverState(self.game))
            self.time_left = 40 * self.game.FPS
    
    def draw_background(self):
        self.game.screen.blit(self.background, (0, 0))

    def draw_question(self):
        question_text = self.font.render(self.questions[self.current_question], True, (255, 255, 255))
        self.game.screen.blit(question_text, ((50, 190)))

    def draw_timer(self):
        progress = self.time_left / (40 * self.game.FPS)
        pygame.draw.rect(self.game.screen, (115, 42, 39), (self.game.WIDTH // 2 - 400, 115, 800, 30), border_radius=20)
        pygame.draw.rect(self.game.screen, (87, 31, 28), (self.game.WIDTH // 2 - 400, 115, int(800 * progress), 30), border_radius=20)

    def draw_lives(self):
        for i in range(self.game.lives):
            self.game.screen.blit(self.game.heart_image, (self.game.WIDTH - (i + 1) * 60 - 50, 62))

    def draw_options(self):
        button_radius = 22
        spacing = 65

        for i, option in enumerate(self.options[self.current_question]):
            y_position = 280 + i * spacing
            pygame.draw.circle(self.game.screen, (255, 255, 255), (70, y_position), button_radius, 1)
            option_text = self.font.render(option, True, (255, 255, 255))
            self.game.screen.blit(option_text, (110, y_position - option_text.get_height() // 2))

    def draw(self):
        self.game.screen.fill((50, 30, 30))
        self.draw_background()
        self.draw_question()
        self.draw_timer()
        self.draw_lives()
        self.draw_options()
        pygame.display.flip()