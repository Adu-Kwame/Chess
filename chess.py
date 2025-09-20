import engine
import pygame #imports 
from aicode import bestMove #imports the minimax algorithm 

WIDTH = HEIGHT = 800
SQ_SIZE = HEIGHT // 8     
sqSelected = ()
playerClicks = []
game = True
moveMade = False

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
white_square = pygame.Surface((SQ_SIZE,SQ_SIZE))
grey_square = pygame.Surface((SQ_SIZE,SQ_SIZE))
white_square.fill('White')
grey_square.fill('grey')
#load images
black_pawn = pygame.image.load('Pieces/black_pawn.png')
white_pawn = pygame.image.load('Pieces/white_pawn.png')
black_bishop = pygame.image.load('Pieces/black_bishop.png')
white_bishop = pygame.image.load('Pieces/white_bishop.png')
black_king = pygame.image.load('Pieces/black_king.png')
white_king = pygame.image.load('Pieces/white_king.png')
white_knight = pygame.image.load('Pieces/white_knight.png')
black_knight = pygame.image.load('Pieces/black_knight.png')
black_queen = pygame.image.load('Pieces/black_queen.png')
white_queen = pygame.image.load('Pieces/white_queen.png')
black_rook = pygame.image.load('Pieces/black_rook.png')
white_rook = pygame.image.load('Pieces/white_rook.png')

pieces = {"black_queen":black_queen, "white_bishop":white_bishop,"white_king": white_king,"white_knight": white_knight,
"white_pawn": white_pawn,"white_rook": white_rook, "black_bishop": black_bishop,"black_king": black_king,
"black_knight": black_knight,"black_rook": black_rook,"black_pawn":black_pawn, "white_queen":white_queen}
 # an error was found as the a sting was given and couldn't load an image with a string so a dictionary was made.
gs = engine.GameState()
validMoves = gs.validMoves()

def place_pieces():
    for row in range(8):
        for col in range(8):
            piece = gs.board[row][col]
            if piece != "e":
                    screen.blit(pieces[piece],(col*SQ_SIZE,row*SQ_SIZE))

def draw_board():
    #creates the squares 
    color = ""
    for row in range(8):
        for col in range(8):
            if (col+row)% 2 == 0: 
                color = "white"
            else:
                color = "grey"
            rect = (col* SQ_SIZE,  row * SQ_SIZE,  SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, color, rect)
def highlightPiece(location):
    if len(location) == 2:
        rect = (location[0]*SQ_SIZE, location[1]* SQ_SIZE, SQ_SIZE, SQ_SIZE)
        color = "light yellow"
        pygame.draw.rect(screen, color, rect)
def choose_gamemode():
    start = False
    while start == False:
        mode = input("One Player? Yes/No:\n")
        if mode.lower == "yes":
            whiteAI = False  
            blackAI = True
            start = True
        elif mode.lower == "no":
            whiteAI = False  
            blackAI = False
            start = True
        else:
            print("Try again")
whiteAI = False  
blackAI = False
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if gs.whiteToMove == False and blackAI == True: 
            AImove = bestMove(gs, validMoves)
            gs.makeMove(AImove)
            moveMade = True
        elif gs.whiteToMove == True and whiteAI == True:  
            AImove = bestMove(gs, validMoves)
            gs.makeMove(AImove)
            moveMade = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_loc = pygame.mouse.get_pos()
            col = mouse_loc[0]// SQ_SIZE
            row = mouse_loc[1]//SQ_SIZE
            if sqSelected == (row,col):
                sqSelected = ()
                playerClicks = []
                highlightPiece(sqSelected)
            else:
                sqSelected = (row,col) 
                playerClicks.append(sqSelected)
            if len(playerClicks) == 2:
                m = engine.Move(playerClicks[0], playerClicks[1], gs.board)
                for x in range(len(validMoves)):
                    if m == validMoves[x]:
                        gs.makeMove(validMoves[x]) #calls the funcion that moves the pieces 
                        playerClicks = []
                        sqSelected = ()
                        moveMade = True
                    else:
                        pass
                if moveMade != True:
                    print("Move not in validMoves")
                    playerClicks = [sqSelected]
    
        if moveMade == True and gs.game == True:
            validMoves = gs.validMoves()  
            moveMade = False
        if gs.checkmate:
            gs.game = False
        if gs.stalemate:
            gs.game = False


    draw_board()
    place_pieces()
   
    pygame.display.update()
    clock.tick(60)