# Inspiração para o codigo: LeMaster Tech
# https://www.youtube.com/watch?v=D8mqgW0DiKk&list=PLsFyHm8kJsx32EFcsJNt5sDI_nKsanRUu&index=17

import pygame
import random
import words

pygame.init()

#cores a serem usadas no jogo
white = (255, 255, 255)
black = (0, 0, 0)
green = (11, 112, 2)
yellow = (204, 207, 43)
gray = (80, 82, 80)
brown = (107, 43, 15)

#definições da tela
width = 500
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Descubra a palavra correta')

background = pygame.image.load('assets/fundo.png')
background = pygame.transform.scale(background, (width, height))

#criação do "tabuleiro"
rowsBoard = [[" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " "],
]

roundGame = 0
fps = 60
timer = pygame.time.Clock()
titleFont = pygame.font.Font('assets/Nunito-SemiBold.ttf', 40)
smallFont = pygame.font.Font('assets/Nunito-SemiBold.ttf', 20)
secretWord = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
gameOver = False
lettersEntered = 0
roundActive = True

def drawRowsBoard():
    global rowsBoard
    global roundGame

    for col in range(0, 5):
        for row in range(0, 6):
            pygame.draw.rect(screen, brown, (col*73 + 74, row*76 + 60, 60, 60), 2, 8)
            
            pieceText = titleFont.render(rowsBoard[row][col], True, white)
            pieceTextRect = pieceText.get_rect(center=(col * 73 + 74 + 30, row * 76 + 58 + 30))
            screen.blit(pieceText, pieceTextRect)

def checkWords():
    global rowsBoard
    global roundGame
    global secretWord

    for col in range(0, 5):
        for row in range(0, 6):
            if secretWord[col] == rowsBoard[row][col] and roundGame > row:
                pygame.draw.rect(screen, green, (col*73 + 74, row*76 + 60, 60, 60), 0, 8) 
            
            elif rowsBoard[row][col] in secretWord and roundGame > row:
                pygame.draw.rect(screen, yellow, (col*73 + 74, row*76 + 60, 60, 60), 0, 8)

            elif rowsBoard[row][col] not in secretWord and roundGame > row:
                pygame.draw.rect(screen, gray, (col*73 + 74, row*76 + 60, 60, 60), 0, 8)

running = True
while running:
    timer.tick(fps)
    screen.fill(white)
    screen.blit(background, (0, 0))
    checkWords()
    drawRowsBoard()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Apagar a ultima letra com a tecla de apagar
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and lettersEntered > 0:
                rowsBoard[roundGame][lettersEntered - 1] = "  "   
                lettersEntered -= 1 

            if event.key == pygame.K_RETURN and not gameOver and lettersEntered >= 5:
                roundGame += 1
                lettersEntered = 0

            if event.key == pygame.K_RETURN and gameOver:
                roundGame = 0
                lettersEntered = 0
                gameOver = False
                secretWord = words.WORDS[random.randint(0, len(words.WORDS) - 1)]
                rowsBoard = [[" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "],
                            [" ", " ", " ", " ", " "]]
                
        if event.type == pygame.TEXTINPUT and roundActive and not gameOver:
            typedText = event.__getattribute__('text')
            rowsBoard[roundGame][lettersEntered] = typedText
            lettersEntered += 1

    for row in range(0, 6):
        guess = rowsBoard[row][0] + rowsBoard[row][1] + rowsBoard[row][2] + rowsBoard[row][3] + rowsBoard[row][4]
        if guess == secretWord and row < roundGame:
            gameOver = True

    if lettersEntered == 5:
        roundActive = False

    if lettersEntered < 5:
        roundActive = True
    
    if roundGame == 6:
        gameOver = True
        gameOverTextWin = smallFont.render('Você não descobriu a palavra correta.', True, white)
        screen.blit(gameOverTextWin, (width/2 - 200, height/2 + 220))
        secretWordText = smallFont.render(f'A palavra era: {secretWord}', True, white)
        screen.blit(secretWordText, (width / 2 - 200, height / 2 + 250))
    
    if gameOver and roundGame < 6:
        gameOverTextLose = smallFont.render('Você descobriu a palavra', True, white)
        screen.blit(gameOverTextLose, (width/2 - 200, height/2 + 220))

    pygame.display.flip()

pygame.quit()