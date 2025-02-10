import pygame
import time
import random
from states.state import State
from states.gameOverState import GameOverState
from states.ticTacToeState import TicTacToeState

class CrosswordsState(State):
    def __init__(self, game):
        super().__init__(game)
        self.WIDTH = 1000
        self.HEIGHT = 600
        self.background = pygame.image.load("assets/backgrounds/background.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        self.palavras = ["livro", "estante", "biblioteca", "texto"]
        self.GRID_SIZE = 10
        self.CELL_SIZE = 45

        self.font = pygame.font.Font("assets/fonts/Poppins-Regular.ttf", 30)
        self.grade = self.criar_grade()
        self.palavras_encontradas = []
        self.tempo_inicial = time.time()
        self.tempo_limite = 300
        self.selecionando = False
        self.selecao = []

    def criar_grade(self):
        grade = [[' ' for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        
        for palavra in self.palavras:
            direcao = random.choice(['horizontal', 'vertical'])
            if direcao == 'horizontal':
                for _ in range(100):  
                    x = random.randint(0, self.GRID_SIZE - len(palavra))
                    y = random.randint(0, self.GRID_SIZE - 1)

                    if all(grade[y][x + i] == ' ' for i in range(len(palavra))):
                        for i, letra in enumerate(palavra):
                            grade[y][x + i] = letra
                        break
            elif direcao == 'vertical':
                for _ in range(100): 
                    x = random.randint(0, self.GRID_SIZE - 1)
                    y = random.randint(0, self.GRID_SIZE - len(palavra))
                    if all(grade[y + i][x] == ' ' for i in range(len(palavra))):
                        for i, letra in enumerate(palavra):
                            grade[y + i][x] = letra
                        break
        
        for y in range(self.GRID_SIZE):
            for x in range(self.GRID_SIZE):
                if grade[y][x] == ' ':
                    grade[y][x] = random.choice('abcdefghijklmnopqrstuvwxyz').lower()
        
        return grade

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    x = (x - 50) // self.CELL_SIZE
                    y = (y - 100) // self.CELL_SIZE
                    if 0 <= x < self.GRID_SIZE and 0 <= y < self.GRID_SIZE:
                        self.selecionando = True
                        self.selecao = [(x, y)]
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.selecionando:
                    self.selecionando = False
                    if self.verificar_palavra():
                        palavra_selecionada = ''.join([self.grade[y][x] for x, y in self.selecao])
                        if palavra_selecionada not in self.palavras_encontradas:
                            self.palavras_encontradas.append(palavra_selecionada)
                    else:
                        self.game.lives -= 1
                        if self.game.lives == 0:
                            self.game.change_state(GameOverState(self.game))
                    self.selecao = []
            elif event.type == pygame.MOUSEMOTION:
                if self.selecionando:
                    x, y = event.pos
                    x = (x - 50) // self.CELL_SIZE
                    y = (y - 100) // self.CELL_SIZE
                    if 0 <= x < self.GRID_SIZE and 0 <= y < self.GRID_SIZE and (x, y) not in self.selecao:
                        self.selecao.append((x, y))

    def verificar_palavra(self):
        letras_selecionadas = [self.grade[y][x] for x, y in self.selecao]
        palavra_selecionada = ''.join(letras_selecionadas)
        return palavra_selecionada in self.palavras or palavra_selecionada[::-1] in self.palavras

    def update(self):
        tempo_restante = int(self.tempo_limite - (time.time() - self.tempo_inicial))
        if tempo_restante <= 0:
            self.game.change_state(GameOverState(self.game))
            
        if len(self.palavras_encontradas) == len(self.palavras):
            self.game.change_state(TicTacToeState(self.game))

    def draw(self):
        self.game.screen.fill((50, 30, 30))
        self.draw_background()
        self.desenhar_grade()
        self.desenhar_hud()
        pygame.display.flip()

    def draw_background(self):
        self.game.screen.blit(self.background, (0, 0))

    def desenhar_grade(self):
        for y in range(self.GRID_SIZE):
            for x in range(self.GRID_SIZE):
                letra = self.grade[y][x]
                cor = (255, 255, 255)
                if (x, y) in self.selecao:
                    cor = (115, 42, 39)
                text = self.font.render(letra, True, cor)
                self.game.screen.blit(text, (x * self.CELL_SIZE + 50, y * self.CELL_SIZE + 100))

    def desenhar_hud(self):
        tempo_restante = int(self.tempo_limite - (time.time() - self.tempo_inicial))
        pygame.draw.rect(self.game.screen, (115, 42, 39), (50, 60, 700, 30), border_radius=10)
        pygame.draw.rect(self.game.screen, (87, 31, 28), (50, 60, int(700 * (tempo_restante / self.tempo_limite)), 30), border_radius=10)

        for i in range(self.game.lives):
            self.game.screen.blit(self.game.heart_image, (self.game.WIDTH - (i + 1) * 60 - 50, 60))

        y_offset = 10  
        textPalavras = self.font.render(f"Palavras encontradas: ", True, (255, 255, 255))
        self.game.screen.blit(textPalavras, (570, 125))
        for i, palavra in enumerate(self.palavras_encontradas):
            text = self.font.render(f"- {palavra}", True, (255, 255, 255))
            self.game.screen.blit(text, (570, y_offset + i * 80 + 160))