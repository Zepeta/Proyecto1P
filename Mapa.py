import numpy as np
import pygame
doc = open("doc.txt","r").read()
filas = doc.split("\n")
row = len(filas)
col = len(filas[0].split(","))
lista = []
for fila in filas:
    aux = fila.split(",")
    for car in aux:
        lista.append(int(car))
mapa = np.array(lista).reshape(row,col)

class Mapa:
    def __init__(self):
        self.mapa = mapa
        self.filas = row
        self.columnas = col
        self.montania = pygame.Surface((30,30))
        self.tierra = pygame.Surface((30,30))
        self.agua = pygame.Surface((30,30))
        self.arena = pygame.Surface((30,30))
        self.bosque = pygame.Surface((30,30))
        self.key = (14,15)
        self.temple = (8,7)
        self.stones = (15,4)
        self.portal = (4,13)
        self.colores = {
            "montania" : (0,0,0),
            "tierra" : (255, 188, 145),
            "agua" : (45,114, 178),
            "arena" : ( 255, 197, 0),
            "bosque" : (29, 220, 32),
        }
        
    def definir_Mapa(self, screen):
        self.montania.fill(self.colores.get("montania"))
        self.tierra.fill(self.colores.get("tierra"))
        self.agua.fill(self.colores.get("agua"))
        self.arena.fill(self.colores.get("arena"))
        self.bosque.fill(self.colores.get("bosque"))
        for i in range(self.filas):
            letra = pygame.font.SysFont(None, 30)
            img = letra.render(str(i+1), True, (0,0,0))
            screen.blit(img, (5, i*30+38))
            screen.blit(img, (i*30+38, 5))
            for j in range(self.columnas):
                if self.mapa[i,j] == 0:
                    screen.blit(self.montania,(j*30+30,i*30+30))             
                elif self.mapa[i,j] == 1:
                    screen.blit(self.tierra,(j*30+30,i*30+30))
                elif self.mapa[i,j] == 2:
                    screen.blit(self.agua,(j*30+30,i*30+30))             
                elif self.mapa[i,j] == 3:
                    screen.blit(self.arena,(j*30+30,i*30+30))             
                elif self.mapa[i,j] == 4:
                    screen.blit(self.bosque,(j*30+30,i*30+30))             
                pygame.draw.line(screen,(0,0,0),(0,j*30+30),(480,j*30+30))
                pygame.draw.line(screen,(0,0,0),(j*30+30,0),(j*30+30,480))
        pygame.draw.line(screen,(0,0,0),(0,480),(480,480))
