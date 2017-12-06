import pygame
import random
import sys
import csv
from pygame.locals import *

# Dimensiones de la pantalla de juego.
SCREEN_WIDTH=600
SCREEN_HEIGHT=900

# Encargada de gestionar el ranking (crearlo, actulizarlo, y guardarlo), de parar el juego y la música.
class GameOver:
    # Creamos el 'gameover' cargando el ranking anterior a la partida.
    def __init__(self,surface, player, font):
        self.font=font
        self.GAMEOVER=False
        with open('.\\data\\marks.csv') as csv_file:    # En el archivo marks.csv guardamos el ranking en formato csv.
            entry=csv.reader(csv_file)
            self.entry=list(entry)
        self.players=[]
        self.players.append(self.font.render("GAMEOVER", 0, (255,0,0))) # Añadimos la cabecera.
    # Paramos el juego, la música y actualizamos el ranking.
    def kill(self,player, mark):
        self.GAMEOVER=True
        player.kill()
        pygame.mixer.music.stop()
        self.calculateRank(player.username, mark)   # Actualizamos el ranking.
        out_csv = open('.\\data\\marks.csv', 'w', newline='')
        out = csv.writer(out_csv)
        out.writerows(self.entry)   # Y lo escribimos.
        del out
        out_csv.close()
    # Recalculamos el ranking dependiendo de la puntuación (mark) que haya obtenido el jugador y creamos los renders de texto  necesarios para mostrarlo.
    def calculateRank(self, username, mark):
        for x in range(5):
            if int(mark) > int(self.entry[x][1]):
                self.entry.pop(x)
                self.entry.insert(x, [username, mark])
                break
        for x in range(5):
            self.players.append(self.font.render(self.entry[x][0]+"     "+str(self.entry[x][1]), 0, (255,0,0)))
    # Refrescamos el ranking en cada frame.
    def update(self, surface):
        if self.GAMEOVER:
            for x in range(6):
                surface.blit(self.players[x], (SCREEN_WIDTH/3,SCREEN_HEIGHT/3+x*30))