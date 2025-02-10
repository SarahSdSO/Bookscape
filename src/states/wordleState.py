import pygame
import random
from states.state import State
from states.gameOverState import GameOverState
from states.hangmanState import HangmanState

class WordleState(State):
    def __init__(self, game):
        super().__init__(game)
        self.WIDTH = 1000
        self.HEIGHT = 600
        self.background = pygame.image.load("assets/backgrounds/background.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.green = (11, 112, 2)
        self.yellow = (204, 207, 43)
        self.gray = (80, 82, 80)
        self.brown = (107, 43, 15)

        self.rowsBoard = [[" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "]]

        self.roundGame = 0
        self.fps = 60
        self.timer = pygame.time.Clock()
        self.titleFont = pygame.font.Font("assets/fonts/Nunito-SemiBold.ttf", 40)
        self.smallFont = pygame.font.Font("assets/fonts/Nunito-SemiBold.ttf", 20)
        self.secretWord = self.get_random_word().upper()  
        self.gameOver = False
        self.lettersEntered = 0
        self.roundActive = True
        self.victory_time = None  
        self.time_left = 120 * self.game.FPS  

        self.board_x = (self.WIDTH - (5 * 73 + 74)) // 2 - 50 
        self.board_y = (self.HEIGHT - (6 * 76 + 60)) // 2

    def get_random_word(self):
        WORDS = [
            "amigo", "autor", "livro", "capas", "citar", "vento", "olhos",
            "copia", "dados", "drama", "eixos", "ideia", "lucro", "justo",
            "notas", "obras", "papel", "poeta", "magia", "matar", "ponte",
            "temas", "texto", "dizer", "estar", "fazer", "beijo", "honra"
        ]
        return random.choice(WORDS)

    def draw_rows_board(self):
        for row in range(0, 6):
            for col in range(0, 5):
                pygame.draw.rect(self.game.screen, self.brown, (self.board_x + col * 73 + 74, self.board_y + row * 76 + 60, 60, 60), 2, 8)
                pieceText = self.titleFont.render(self.rowsBoard[row][col], True, self.white)
                pieceTextRect = pieceText.get_rect(center=(self.board_x + col * 73 + 74 + 30, self.board_y + row * 76 + 58 + 30))
                self.game.screen.blit(pieceText, pieceTextRect)

    def check_words(self):
        for row in range(0, 6):
            if self.roundGame > row:
                guess = "".join(self.rowsBoard[row]).strip()
                if guess == self.secretWord:
                    for col in range(0, 5):
                        pygame.draw.rect(self.game.screen, self.green, (self.board_x + col * 73 + 74, self.board_y + row * 76 + 60, 60, 60), 0, 8)
                else:
                    for col in range(0, 5):
                        if self.rowsBoard[row][col] == self.secretWord[col]:
                            pygame.draw.rect(self.game.screen, self.green, (self.board_x + col * 73 + 74, self.board_y + row * 76 + 60, 60, 60), 0, 8)
                            
                        elif self.rowsBoard[row][col] in self.secretWord:
                            pygame.draw.rect(self.game.screen, self.yellow, (self.board_x + col * 73 + 74, self.board_y + row * 76 + 60, 60, 60), 0, 8)
                        else:
                            pygame.draw.rect(self.game.screen, self.gray, (self.board_x + col * 73 + 74, self.board_y + row * 76 + 60, 60, 60), 0, 8)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and self.lettersEntered > 0:
                    self.rowsBoard[self.roundGame][self.lettersEntered - 1] = " "
                    self.lettersEntered -= 1

                if event.key == pygame.K_RETURN and not self.gameOver and self.lettersEntered == 5:
                    guess = "".join(self.rowsBoard[self.roundGame]).strip()
                    if guess == self.secretWord:
                        self.gameOver = True
                        self.victory_time = pygame.time.get_ticks()  
                        self.game.change_state(HangmanState(self.game))  
                    else:
                        self.roundGame += 1
                        self.lettersEntered = 0
                        if self.roundGame == 6:
                            self.gameOver = True
                            self.game.lives -= 1
                            if self.game.lives == 0:
                                self.game.change_state(GameOverState(self.game))
                            else:
                                self.reset_game()

                if event.key == pygame.K_RETURN and self.gameOver:
                    if "".join(self.rowsBoard[self.roundGame - 1]).strip() != self.secretWord:
                        self.reset_game()

            if event.type == pygame.TEXTINPUT and self.roundActive and not self.gameOver:
                typedText = event.__getattribute__('text').upper()  
                if self.lettersEntered < 5:
                    self.rowsBoard[self.roundGame][self.lettersEntered] = typedText
                    self.lettersEntered += 1

    def update(self):
        if self.gameOver and self.victory_time:
            if pygame.time.get_ticks() - self.victory_time > 5000:  
                self.game.change_state(HangmanState(self.game))

        if self.time_left > 0:
            self.time_left -= 1
        else:
            self.gameOver = True
            self.game.lives -= 1
            if self.game.lives == 0:
                self.game.change_state(GameOverState(self.game))
            else:
                self.reset_game()

    def draw(self):
        self.game.screen.blit(self.background, (0, 0))
        self.check_words()
        self.draw_rows_board()

        if self.gameOver:
            if "".join(self.rowsBoard[self.roundGame - 1]).strip() == self.secretWord:
                game_over_text = self.smallFont.render("Você descobriu a palavra!", True, self.white)
                self.game.screen.blit(game_over_text, (self.WIDTH / 2 - 150, self.HEIGHT / 2 + 220))
            else:
                game_over_text = self.smallFont.render("Você não descobriu a palavra correta.", True, self.white)
                self.game.screen.blit(game_over_text, (self.WIDTH / 2 - 200, self.HEIGHT / 2 + 220))
                secret_word_text = self.smallFont.render(f"A palavra era: {self.secretWord}", True, self.white)
                self.game.screen.blit(secret_word_text, (self.WIDTH / 2 - 200, self.HEIGHT / 2 + 250))

        for i in range(self.game.lives):
            self.game.screen.blit(self.game.heart_image, (self.WIDTH - (i + 1) * 45 - 50, 60))

        progress = self.time_left / (120 * self.game.FPS)
        pygame.draw.rect(self.game.screen, (115, 42, 39), (self.WIDTH // 2 - 300, 60, 600, 20), border_radius=10)  
        pygame.draw.rect(self.game.screen, (87, 31, 28), (self.WIDTH // 2 - 300, 60, int(600 * progress), 20), border_radius=10)

        pygame.display.flip()

    def reset_game(self):
        self.roundGame = 0
        self.lettersEntered = 0
        self.gameOver = False
        self.victory_time = None
        self.time_left = 120 * self.game.FPS  
        self.secretWord = self.get_random_word().upper()  
        self.rowsBoard = [[" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "],
                         [" ", " ", " ", " ", " "]]