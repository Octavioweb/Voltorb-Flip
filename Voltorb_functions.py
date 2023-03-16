import pygame, random, sys
from pygame.locals import*

#DESOCUPADA
def DrawMainBoard(BOARDSIZE, TILESIZE, GAPSIZE, DISPLAYSURF, BLACK): # No se repite
    for i in range (BOARDSIZE):
        for j in range (BOARDSIZE):
            pygame.draw.rect(DISPLAYSURF, BLACK, (GAPSIZE+(GAPSIZE+TILESIZE)*i,GAPSIZE+(GAPSIZE+TILESIZE)*j , TILESIZE, TILESIZE))

def DrawVoltorbTiles(VOLTORBTILES, DISPLAYSURF, GREEN, BLUE, GAPSIZE, TILESIZE, BOARDSIZE): #No se repite
    for i in range (VOLTORBTILES):
        if i <= BOARDSIZE -1 :
            pygame.draw.rect(DISPLAYSURF, GREEN, (GAPSIZE+(GAPSIZE+TILESIZE)*i,BOARDSIZE*(GAPSIZE+TILESIZE)+GAPSIZE , TILESIZE, TILESIZE))
        elif i :
            pygame.draw.rect(DISPLAYSURF, BLUE, (BOARDSIZE*(GAPSIZE+TILESIZE)+GAPSIZE, GAPSIZE+((GAPSIZE+TILESIZE)*(i-BOARDSIZE-1)) , TILESIZE, TILESIZE))

def CreateVoltorbDefaultText(VOLTORBTILES, TILESIZE, BLACK): #No se repite
    font = pygame.font.Font('Pixel Sans Serif.ttf', int(TILESIZE/3)) #El tamaño del texto crece con el tilesize
    voltorbfonts_list = []
    for i in range (VOLTORBTILES):
        voltorbfonts_list.append([str(i), False, BLACK])
    return (font, voltorbfonts_list)

def GetVoltorbNumbers(): #No se repite
    global voltorbPerLine
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
    #print (voltorbPerLine)

def CreateBackBoard(BOARDSIZE, DIFFICULTY): # No se repite
    global tablero
    tablero = []
    for i in range(BOARDSIZE):
        renglon = []
        for j in range(BOARDSIZE):
            choices = ['X' for i in range(DIFFICULTY)]
            choices_temp = ['O' for j in range(10-DIFFICULTY)]
            choices.extend(choices_temp)
            rando = random.choice(choices)
            renglon.append(rando)
        tablero.append(renglon)
    return tablero