import pygame
import random
from states.state import State
from states.gameOverState import GameOverState
from states.winningState import WinningState

class HangmanState(State):
    def __init__(self, game):
        super().__init__(game)
        self.WIDTH = 1000
        self.HEIGHT = 600
        self.background = pygame.image.load("assets/backgrounds/background.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        
        self.font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 36)
        self.small_font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 25)

        self.palavras = [
            "livro", "biblioteca", "romance", "poesia", "autor", "editora", "leitura",
            "estante", "página", "capitulo", "literatura", "personagem", "antagonista"
        ]

        self.tentativas_maximas = 6
        self.rodadas_totais = 5
        self.rodada_atual = 1
        self.palavra_secreta = self.escolher_palavra()
        self.letras_corretas = []
        self.letras_erradas = []
        self.tentativas = 0
        self.time_left = 60 * self.game.FPS
    
    def escolher_palavra(self):
        return random.choice(self.palavras)

    def desenhar_forca(self):
        base_y_offset = 58 
        if self.tentativas >= 1:
            pygame.draw.line(self.game.screen, (255, 255, 255), (100, 450 + base_y_offset), (300, 450 + base_y_offset), 5)  # Base
        if self.tentativas >= 2:
            pygame.draw.line(self.game.screen, (255, 255, 255), (200, 450 + base_y_offset), (200, 50 + base_y_offset), 5)  # Poste
        if self.tentativas >= 3:
            pygame.draw.line(self.game.screen, (255, 255, 255), (200, 50 + base_y_offset), (400, 50 + base_y_offset), 5)  # Topo
        if self.tentativas >= 4:
            pygame.draw.line(self.game.screen, (255, 255, 255), (400, 50 + base_y_offset), (400, 100 + base_y_offset), 5)  # Corda
        if self.tentativas >= 5:
            pygame.draw.circle(self.game.screen, (255, 255, 255), (400, 130 + base_y_offset), 30, 5)  # Cabeça
        if self.tentativas >= 6:
            pygame.draw.line(self.game.screen, (255, 255, 255), (400, 160 + base_y_offset), (400, 300 + base_y_offset), 5)  # Corpo
            pygame.draw.line(self.game.screen, (255, 255, 255), (400, 200 + base_y_offset), (350, 150 + base_y_offset), 5)  # Braço esquerdo
            pygame.draw.line(self.game.screen, (255, 255, 255), (400, 200 + base_y_offset), (450, 150 + base_y_offset), 5)  # Braço direito
            pygame.draw.line(self.game.screen, (255, 255, 255), (400, 300 + base_y_offset), (350, 350 + base_y_offset), 5)  # Perna esquerda
            pygame.draw.line(self.game.screen, (255, 255, 255), (400, 300 + base_y_offset), (450, 350 + base_y_offset), 5)  # Perna direita
    
    def desenhar_palavra(self):
        display_palavra = " ".join([letra if letra in self.letras_corretas else "_" for letra in self.palavra_secreta])
        texto = self.font.render(display_palavra, True, (255, 255, 255))
        self.game.screen.blit(texto, (100, 509))

    def desenhar_letras_erradas(self):
        texto = self.small_font.render("Letras erradas: " + ", ".join(self.letras_erradas), True, (148, 72, 69))
        self.game.screen.blit(texto, (600, 220))
    
    def desenhar_timer(self):
        progress = self.time_left / (60 * self.game.FPS)
        pygame.draw.rect(self.game.screen, (115, 42, 39), (self.WIDTH // 2 - 330, 65, 600, 20), border_radius=10)
        pygame.draw.rect(self.game.screen, (87, 31, 28), (self.WIDTH // 2 - 330, 65, int(600 * progress), 20), border_radius=10)
    
    def desenhar_vidas(self):
        for i in range(self.game.lives):
            self.game.screen.blit(self.game.heart_image, (self.WIDTH - (i + 1) * 45 - 50, 60))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if pygame.K_a <= event.key <= pygame.K_z:
                    letra = chr(event.key).lower()
                    if letra in self.palavra_secreta and letra not in self.letras_corretas:
                        self.letras_corretas.append(letra)
                    elif letra not in self.palavra_secreta and letra not in self.letras_erradas:
                        self.letras_erradas.append(letra)
                        self.tentativas += 1
    
    def update(self):
        if all(letra in self.letras_corretas for letra in self.palavra_secreta):
            self.rodada_atual += 1
            if self.rodada_atual > self.rodadas_totais:
                self.game.change_state(WinningState(self.game))
            else:
                self.reset_rodada()
        
        if self.tentativas >= self.tentativas_maximas or self.time_left <= 0:
            self.game.lives -= 1
            if self.game.lives == 0:
                self.game.change_state(GameOverState(self.game))
            else:
                self.reset_rodada()
        
        if self.time_left > 0:
            self.time_left -= 1
    
    def draw(self):
        self.game.screen.blit(self.background, (0, 0))
        self.desenhar_forca()
        self.desenhar_palavra()
        self.desenhar_letras_erradas()
        self.desenhar_timer()
        self.desenhar_vidas()
        pygame.display.flip()
    
    def reset_rodada(self):
        self.palavra_secreta = self.escolher_palavra()
        self.letras_corretas = []
        self.letras_erradas = []
        self.tentativas = 0
        self.time_left = 60 * self.game.FPS