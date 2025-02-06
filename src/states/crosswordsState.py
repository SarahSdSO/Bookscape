import pygame
import random
import time
from gameState import GameState

class CrosswordsState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.lives = game.current_state.lives

    def enter(self):
        # Fecha a janela do Tkinter antes de iniciar o Pygame
        self.game.root.destroy()
        self.run_crosswords()

    def run_crosswords(self):
        pygame.init()
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Caça-Palavras - Biblioteca")

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)

        font = pygame.font.SysFont("Arial", 40)
        small_font = pygame.font.SysFont("Arial", 20)

        palavras = ["livro", "estante", "leitura", "biblioteca", "autor", "editora", "pagina", "capitulo", "texto", "pesquisa"]

        GRID_SIZE = 10
        CELL_SIZE = 50

        def criar_grade():
            grade = [[random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
            for palavra in palavras:
                direcao = random.choice(['horizontal', 'vertical', 'diagonal'])
                if direcao == 'horizontal':
                    x = random.randint(0, GRID_SIZE - len(palavra))
                    y = random.randint(0, GRID_SIZE - 1)
                    for i, letra in enumerate(palavra):
                        grade[y][x + i] = letra
                elif direcao == 'vertical':
                    x = random.randint(0, GRID_SIZE - 1)
                    y = random.randint(0, GRID_SIZE - len(palavra))
                    for i, letra in enumerate(palavra):
                        grade[y + i][x] = letra
                elif direcao == 'diagonal':
                    x = random.randint(0, GRID_SIZE - len(palavra))
                    y = random.randint(0, GRID_SIZE - len(palavra))
                    for i, letra in enumerate(palavra):
                        grade[y + i][x + i] = letra
            return grade

        def desenhar_grade(grade, selecao=None):
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    letra = grade[y][x]
                    cor = BLACK
                    if selecao and (x, y) in selecao:
                        cor = BLUE
                    text = font.render(letra, True, cor)
                    screen.blit(text, (x * CELL_SIZE + 50, y * CELL_SIZE + 50))

        def verificar_palavra(palavra, grade, selecao):
            letras_selecionadas = [grade[y][x] for x, y in selecao]
            palavra_selecionada = ''.join(letras_selecionadas)
            return palavra_selecionada == palavra

        grade = criar_grade()
        palavras_encontradas = []
        tentativas = self.lives
        tempo_inicial = time.time()
        tempo_limite = 300

        selecionando = False
        selecao = []

        running = True
        while running:
            screen.fill(WHITE)
            desenhar_grade(grade, selecao)

            text = small_font.render(f"Palavras encontradas: {', '.join(palavras_encontradas)}", True, BLACK)
            screen.blit(text, (50, 10))

            text = small_font.render(f"Tentativas restantes: {tentativas}", True, BLACK)
            screen.blit(text, (50, 30))

            tempo_restante = int(tempo_limite - (time.time() - tempo_inicial))
            text = small_font.render(f"Tempo restante: {tempo_restante}s", True, BLACK)
            screen.blit(text, (50, 50))

            if tempo_restante <= 0:
                text = font.render("Tempo esgotado!", True, RED)
                screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False

            if len(palavras_encontradas) == len(palavras):
                text = font.render("Parabéns! Você venceu!", True, GREEN)
                screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        selecionando = True
                        selecao = []
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        selecionando = False
                        palavra_selecionada = ''.join([grade[y][x] for x, y in selecao])
                        if palavra_selecionada in palavras and palavra_selecionada not in palavras_encontradas:
                            palavras_encontradas.append(palavra_selecionada)
                        else:
                            tentativas -= 1
                            if tentativas == 0:
                                text = font.render("Você perdeu!", True, RED)
                                screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))
                                pygame.display.flip()
                                pygame.time.wait(3000)
                                running = False
                        selecao = []
                if event.type == pygame.MOUSEMOTION:
                    if selecionando:
                        x, y = event.pos
                        x = (x - 50) // CELL_SIZE
                        y = (y - 50) // CELL_SIZE
                        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and (x, y) not in selecao:
                            selecao.append((x, y))

            pygame.display.flip()

        pygame.quit()
        if len(palavras_encontradas) == len(palavras):
            from states.winningState import WinningState
            self.game.change_state(WinningState(self.game))
        else:
            from states.gameOverState import GameOverState
            self.game.change_state(GameOverState(self.game))