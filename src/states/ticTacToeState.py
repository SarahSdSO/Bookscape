import pygame
import random
from states.state import State
from states.wordleState import WordleState
from states.gameOverState import GameOverState

class TicTacToeState(State):
    def __init__(self, game):
        super().__init__(game)
        self.WIDTH, self.HEIGHT = 500, 500
        self.LINE_WIDTH = 5
        self.BOARD_ROWS, self.BOARD_COLS = 3, 3
        self.SQUARE_SIZE = self.WIDTH // self.BOARD_COLS

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.background = pygame.image.load("assets/backgrounds/background.png")  
        self.background = pygame.transform.scale(self.background, (self.game.WIDTH, self.game.HEIGHT))
        self.paper_img = pygame.image.load("assets/backgrounds/paper.png")
        self.pen_img = pygame.image.load("assets/backgrounds/pen.png")
        self.paper_img = pygame.transform.scale(self.paper_img, (self.SQUARE_SIZE, self.SQUARE_SIZE))
        self.pen_img = pygame.transform.scale(self.pen_img, (self.SQUARE_SIZE, self.SQUARE_SIZE))

        self.game_area = pygame.Rect(
            (self.game.WIDTH - self.WIDTH) // 2,  
            (self.game.HEIGHT - self.HEIGHT) // 2,  
            self.WIDTH,  
            self.HEIGHT  
        )

        self.board = [[None for _ in range(self.BOARD_COLS)] for _ in range(self.BOARD_ROWS)]
        self.player = random.choice(["paper", "pen"])
        self.ai = "pen" if self.player == "paper" else "paper"
        self.game_over = False
        self.winner = None

    def draw_lines(self):
        start_x = self.game_area.x
        start_y = self.game_area.y
        for i in range(1, self.BOARD_ROWS):
            pygame.draw.line(
                self.game.screen, self.WHITE,
                (start_x, start_y + i * self.SQUARE_SIZE),
                (start_x + self.WIDTH, start_y + i * self.SQUARE_SIZE),
                self.LINE_WIDTH
            )
        for i in range(1, self.BOARD_COLS):
            pygame.draw.line(
                self.game.screen, self.WHITE,
                (start_x + i * self.SQUARE_SIZE, start_y),
                (start_x + i * self.SQUARE_SIZE, start_y + self.HEIGHT),
                self.LINE_WIDTH
            )

    def draw_icons(self):
        start_x = self.game_area.x
        start_y = self.game_area.y
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if self.board[row][col] == "paper":
                    self.game.screen.blit(
                        self.paper_img,
                        (start_x + col * self.SQUARE_SIZE, start_y + row * self.SQUARE_SIZE)
                    )
                elif self.board[row][col] == "pen":
                    self.game.screen.blit(
                        self.pen_img,
                        (start_x + col * self.SQUARE_SIZE, start_y + row * self.SQUARE_SIZE)
                    )

    def check_winner(self):
        for row in range(self.BOARD_ROWS):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] and self.board[row][0] is not None:
                return self.board[row][0]

        for col in range(self.BOARD_COLS):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                return self.board[0][col]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return self.board[0][2]

        if all(self.board[row][col] is not None for row in range(self.BOARD_ROWS) for col in range(self.BOARD_COLS)):
            return "tie"

        return None

    def evaluate_board(self):
        # Avaliar o tabuleiro para o algoritmo Minimax
        winner = self.check_winner()
        if winner == self.ai:
            return 1
        elif winner == self.player:
            return -1
        elif winner == "tie":
            return 0
        else:
            return None

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        # Algoritmo Minimax
        result = self.evaluate_board()
        if result is not None:
            return result

        if is_maximizing:
            best_score = -float("inf")
            for row in range(self.BOARD_ROWS):
                for col in range(self.BOARD_COLS):
                    if board[row][col] is None:
                        board[row][col] = self.ai
                        score = self.minimax(board, depth + 1, False, alpha, beta)
                        board[row][col] = None
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = float("inf")
            for row in range(self.BOARD_ROWS):
                for col in range(self.BOARD_COLS):
                    if board[row][col] is None:
                        board[row][col] = self.player
                        score = self.minimax(board, depth + 1, True, alpha, beta)
                        board[row][col] = None
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score

    def ai_move(self):
        # Movimento da IA usando Minimax
        best_score = -float("inf")
        best_move = None

        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if self.board[row][col] is None:
                    self.board[row][col] = self.ai
                    score = self.minimax(self.board, 0, False, -float("inf"), float("inf"))
                    self.board[row][col] = None
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        if best_move:
            self.board[best_move[0]][best_move[1]] = self.ai

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                mouseX, mouseY = event.pos
                if self.game_area.collidepoint(mouseX, mouseY):
                    clicked_row = (mouseY - self.game_area.y) // self.SQUARE_SIZE
                    clicked_col = (mouseX - self.game_area.x) // self.SQUARE_SIZE

                    if self.board[clicked_row][clicked_col] is None:
                        self.board[clicked_row][clicked_col] = self.player
                        self.winner = self.check_winner()
                        if self.winner:
                            self.game_over = True
                        else:
                            self.ai_move()
                            self.winner = self.check_winner()
                            if self.winner:
                                self.game_over = True

    def update(self):
        if self.game_over:
            if self.winner == self.player:
                self.game.change_state(WordleState(self.game))

            elif self.winner == "tie":
                self.game.change_state(TicTacToeState(self.game))

            else:
                self.game.lives -= 1
                if self.game.lives == 0:
                    self.game.change_state(GameOverState(self.game))
                else:
                    self.game.change_state(TicTacToeState(self.game))

    def draw(self):
        self.game.screen.blit(self.background, (0, 0))

        self.draw_lines()
        self.draw_icons()

        if self.game_over:
            font = pygame.font.Font(None, 36)
            if self.winner == "tie":
                text = font.render("Empate!", True, self.BLACK)
            else:
                text = font.render(f"{self.winner.capitalize()} Venceu!", True, self.BLACK)
            self.game.screen.blit(text, (self.game.WIDTH // 2 - text.get_width() // 2, self.game.HEIGHT // 2 - text.get_height() // 2))

        for i in range(self.game.lives):
            self.game.screen.blit(self.game.heart_image, (self.game.WIDTH - (i + 1) * 60 - 10, 20))

        pygame.display.flip()