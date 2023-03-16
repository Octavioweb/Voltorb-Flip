#Copia de juego Voltorb Flip usando pygame 
import pygame, random, sys
import Voltorb_functions as V_once
from pygame.locals import*

mines_output = open('Minas.txt', 'w')
archivoLargo = open('Textolargo.txt', 'w')
fps = 60

DIFFICULTY = 3 # Un número entre 0 (fácil) y 10 (literal imposible)
BOARDSIZE = 5
WINSIZE = 650 #Un número que dé un GAPSIZE un número entero
TILESIZE = (WINSIZE/(BOARDSIZE+2)) #Se le suma 1 por los espacios hasta la derecha y abajo, donde están los números
GAPSIZE = ((WINSIZE-((BOARDSIZE+1)*TILESIZE)))/(BOARDSIZE+2) 
print (GAPSIZE)
VOLTORBTILES = ((BOARDSIZE+1)**2)-(BOARDSIZE**2)
print (VOLTORBTILES)

#COLOR     R    G    B
BLACK =  (0,    0,    0)
WHITE =  (255, 255, 255)
BLUE  =  (0,   0,   255)
GREEN =  (0,   255,   0)
DARK_GREEN = (0, 255, 100)
DARK_GRAY = (80, 80, 80)
RED = (255, 0, 0)

def Main():
    global DISPLAYSURF, FPSCLOCK
    DISPLAYSURF = pygame.display.set_mode((WINSIZE, WINSIZE))
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Voltorb Flip')
    pygame.init()
    boxx = None
    boxy = None
    DISPLAYSURF.fill ((200, 200, 200))
    mousex, mousey = 0, 0
    click = False
    tablero = V_once.CreateBackBoard(BOARDSIZE, DIFFICULTY)
    
    for line in tablero:
        print (line, end = '\n ', file =mines_output)
        
    font, voltorbfonts_list = V_once.CreateVoltorbDefaultText(VOLTORBTILES, TILESIZE, BLACK) #Importar color
    #V_once.DrawMainBoard(BOARDSIZE, TILESIZE, GAPSIZE, DISPLAYSURF, BLACK) #Importar color

    V_once.DrawVoltorbTiles(VOLTORBTILES, DISPLAYSURF, GREEN, BLUE, GAPSIZE, TILESIZE, BOARDSIZE)
    revealedList = [[False,]*BOARDSIZE for P in range (BOARDSIZE)] #Crea lista de cajas reveladas

    mines_output.close()

    while True:
        for event in pygame.event.get(): 
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                click = True
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                click = False
#         for r in revealedList:
#             print (r)
        boxx, boxy = GetBoxAtMouse(mousex, mousey)
#        print (boxx, boxy, mousex, mousey, click)

        if (boxx != None) and revealedList[boxy][boxx] == False and click == False:
            CreateHighlight(boxx, boxy)
        elif (boxx != None) and revealedList[boxy][boxx] == False and click == True:
             revealedList[boxy][boxx] = True
             if revealedList[boxy][boxx] == True and tablero[boxy][boxx] == 'X':
                 print ('dead', boxx, boxy)
                 pygame.quit()
                 archivoLargo.close()
                 sys.exit()
        
        UpdateBoard(revealedList, boxx, boxy)
        UpdateVoltorbText(tablero, voltorbfonts_list, font)
        print (mousex, mousey, tablero, revealedList, voltorbfonts_list, '\n', file = archivoLargo)
        pygame.display.update()
        FPSCLOCK.tick(fps)
    
def UpdateVoltorbText(tablero, fonts_list, font): #Se repite
    voltorbPerLine = GetVoltorbNumbers(tablero)
    for i in fonts_list:
        j = (fonts_list.index(i))
        try:
            text = str(voltorbPerLine[j])
        except:
            continue
        temp_texto = font.render(text, i[1], i[2])
        temp_rect = temp_texto.get_rect()
        
        if j == (VOLTORBTILES-1):
            continue
        elif j <= int(BOARDSIZE-1):
            centerx = ((0.5*TILESIZE)+GAPSIZE+(GAPSIZE+TILESIZE)*j)
            centery = ((0.4*TILESIZE)+(BOARDSIZE*(GAPSIZE+TILESIZE)))
        else:
            centerx = ((0.6*TILESIZE)+(BOARDSIZE*(GAPSIZE+TILESIZE)))
            centery = ((0.3*TILESIZE)+GAPSIZE+(GAPSIZE+TILESIZE)*(j-BOARDSIZE))
            
        temp_rect.center = (centerx, centery)
        DISPLAYSURF.blit(temp_texto, temp_rect)
        
def GetBoxAtMouse(mousex, mousey): # Se repite
    for i in range (BOARDSIZE):
        for j in range (BOARDSIZE):
            temp_rect = pygame.Rect(GAPSIZE+(GAPSIZE+TILESIZE)*i,GAPSIZE+(GAPSIZE+TILESIZE)*j , TILESIZE, TILESIZE)
            if temp_rect.collidepoint(mousex, mousey):
                return (i, j)        
    return (None,None)

def CreateHighlight(i, j):    
    pygame.draw.rect (DISPLAYSURF, DARK_GRAY, ((GAPSIZE+(GAPSIZE+TILESIZE)*i,GAPSIZE+(GAPSIZE+TILESIZE)*j , TILESIZE, TILESIZE)))
    #pygame.display.update()
    
def UpdateBoard(revealedList, boxx, boxy): #Se repite
    for i in range(BOARDSIZE):
        for j in range(BOARDSIZE):
            if revealedList[j][i] == True:
                pygame.draw.rect (DISPLAYSURF, WHITE, ((GAPSIZE+(GAPSIZE+TILESIZE)*i,GAPSIZE+(GAPSIZE+TILESIZE)*j , TILESIZE, TILESIZE)))
    
            elif revealedList[j][i] == False and i != boxx and j != boxy:
                pygame.draw.rect (DISPLAYSURF, BLACK, ((GAPSIZE+(GAPSIZE+TILESIZE)*i,GAPSIZE+(GAPSIZE+TILESIZE)*j , TILESIZE, TILESIZE)))
    
    
def GetVoltorbNumbers(tablero): #Sí se repite, dentro de UpdateVoltorbText()
    voltorbPerLine = {}
    for i in range(VOLTORBTILES-1):
        if i <= BOARDSIZE-1:
            voltorbPerLine[i+BOARDSIZE] = tablero[i].count('X')
        else:
            value_res = 0
            for j in range(BOARDSIZE):
                if tablero[j][i-BOARDSIZE] == 'X':  
                    value_res += 1
    #                print (i-BOARDSIZE, j, value_res)
            voltorbPerLine[i-BOARDSIZE] = value_res
    return voltorbPerLine

if __name__ == '__main__':
    Main()
