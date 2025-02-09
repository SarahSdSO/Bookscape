import pygame
from states.state import State
from states.quizState import QuizState

class StoryState(State):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 24)
        self.ok_button = pygame.Rect(self.game.WIDTH // 2 - 50, self.game.HEIGHT - 150, 100, 50)
        self.next_button = pygame.Rect(self.game.WIDTH // 2 - 100, self.game.HEIGHT - 150, 200, 50)

        self.story_parts = [
            "Você adora passar horas na biblioteca da cidade, mas, dessa vez, algo mágico acontece. "
            "Ao puxar um livro antigo de uma prateleira, o chão sob seus pés treme, e você se vê transportado para outro lugar. "
            "As estantes se estendem e flutuam no ar, até que uma figura encapuzada surge diante de você:",

            "— Bem-vindo à Biblioteca dos Perdidos. Há séculos, livros importantes desapareceram do mundo, "
            "e apenas quem provar seu valor pode restaurá-los. Você aceita o desafio?",

            "Cada prateleira esconde um enigma, um desafio que deve ser resolvido para restaurar um livro perdido. "
            "Somente ao recuperar todas as histórias desaparecidas, você encontrará a saída desse mundo literário."
        ]

        self.current_part = 0 
        self.text_to_display = "" 
        self.text_index = 0  
        self.show_button = False 
        self.text_speed = 1.2  
        self.last_update_time = pygame.time.get_ticks()

        self.background_image = pygame.image.load("assets/backgrounds/background.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.game.WIDTH, self.game.HEIGHT))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
                pygame.mixer.music.stop()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.show_button:
                    if self.current_part < len(self.story_parts) - 1 and self.ok_button.collidepoint(event.pos):
                        self.current_part += 1
                        self.text_to_display = ""
                        self.text_index = 0
                        self.show_button = False

                    elif self.current_part == len(self.story_parts) - 1 and self.next_button.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        self.game.change_state(QuizState(self.game))


    def update(self):
        current_time = pygame.time.get_ticks()
        if self.text_index < len(self.story_parts[self.current_part]) and current_time - self.last_update_time > 50 // self.text_speed:
            self.text_to_display += self.story_parts[self.current_part][self.text_index]
            self.text_index += 1
            self.last_update_time = current_time

        elif self.text_index >= len(self.story_parts[self.current_part]):
            self.show_button = True

    def draw(self):
        self.game.screen.blit(self.background_image, (0, 0))

        dialog_box = pygame.Rect(50, self.game.HEIGHT // 2 - 100, self.game.WIDTH - 100, 200)
        pygame.draw.rect(self.game.screen, (87, 31, 28), dialog_box)
        pygame.draw.rect(self.game.screen, (255, 255, 255), dialog_box, 3)

        text_surface = self.render_wrapped_text(self.text_to_display, dialog_box)
        self.game.screen.blit(text_surface, (dialog_box.x + 20, dialog_box.y + 20))

        mouse_pos = pygame.mouse.get_pos()

        if self.show_button:
            if self.current_part < len(self.story_parts) - 1:
                button_color = (67, 21, 18) if self.ok_button.collidepoint(mouse_pos) else (87, 31, 28)
                pygame.draw.rect(self.game.screen, button_color, self.ok_button, border_radius=10)
                ok_text = self.font.render("OK", True, (255, 255, 255))
                ok_text_rect = ok_text.get_rect(center=self.ok_button.center)
                self.game.screen.blit(ok_text, ok_text_rect)
            else:
                button_color = (67, 21, 18) if self.next_button.collidepoint(mouse_pos) else (87, 31, 28)
                pygame.draw.rect(self.game.screen, button_color, self.next_button, border_radius=10)
                next_text = self.font.render("->", True, (255, 255, 255))
                next_text_rect = next_text.get_rect(center=self.next_button.center)
                self.game.screen.blit(next_text, next_text_rect)

        pygame.display.flip()

    def render_wrapped_text(self, text, rect):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] < rect.width - 40:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        surface = pygame.Surface((rect.width - 40, rect.height - 40), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        y = 0
        for line in lines:
            line_surface = self.font.render(line, True, (255, 255, 255))
            surface.blit(line_surface, (0, y))
            y += self.font.size(line)[1]
        return surface