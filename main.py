import pygame, sys
 
pygame.init()
 
WIDTH, HEIGHT = 900, 900
 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE|pygame.DOUBLEBUF|pygame.HWSURFACE)
pygame.display.set_caption("Tic Tac Toe!")
 
BOARD = pygame.image.load("assets/Board.png")
X_IMG = pygame.image.load("assets/X.png")
O_IMG = pygame.image.load("assets/O.png")
 
BG_COLOR = (214, 201, 227)
 
board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
graphical_board = [[[None, None], [None, None], [None, None]], 
                    [[None, None], [None, None], [None, None]], 
                    [[None, None], [None, None], [None, None]]]
 
to_move = 'X'
 
SCREEN.fill(BG_COLOR)
SCREEN.blit(pygame.transform.scale(BOARD, (WIDTH, HEIGHT)), (0, 0))
 
pygame.display.update()

def adjust_mouse_pos():
    print(pygame.mouse.get_pos())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            SCREEN = pygame.display.set_mode(event.size, flags=pygame.RESIZABLE|pygame.DOUBLEBUF|pygame.HWSURFACE)
            SCREEN.fill(BG_COLOR)
            SCREEN.blit(pygame.transform.scale(BOARD, event.size), (0, 0))
            pygame.display.update()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
